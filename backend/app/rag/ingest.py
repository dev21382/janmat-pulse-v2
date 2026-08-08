import json
import logging

import httpx
from pypdf import PdfReader
import io
import ftfy

from app.config import MANIFESTO_DIR
from app.rag.sources import MANIFESTOS

log = logging.getLogger("rag.ingest")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
}


def _pdf_path(party_id: str):
    return MANIFESTO_DIR / f"{party_id}.pdf"


def _text_path(party_id: str):
    return MANIFESTO_DIR / f"{party_id}.txt"


def _pages_path(party_id: str):
    return MANIFESTO_DIR / f"{party_id}.pages.json"


def download_manifesto(source: dict, timeout: float = 90.0) -> bool:
    party_id = source["party_id"]
    text_path = _text_path(party_id)
    if text_path.exists():
        return True

    try:
        with httpx.Client(headers=HEADERS, timeout=timeout, follow_redirects=True) as client:
            resp = client.get(source["url"])
            resp.raise_for_status()
            pdf_bytes = resp.content
    except Exception as exc:
        log.warning("manifesto download failed party=%s err=%s", party_id, exc)
        return False

    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages = [ftfy.fix_text(page.extract_text() or "") for page in reader.pages]
        text = "\n\n".join(pages)
    except Exception as exc:
        log.warning("manifesto pdf parse failed party=%s err=%s", party_id, exc)
        return False

    if len(text.strip()) < 500:
        log.warning("manifesto text suspiciously short party=%s len=%d", party_id, len(text))
        return False

    _pdf_path(party_id).write_bytes(pdf_bytes)
    text_path.write_text(text, encoding="utf-8")
    _pages_path(party_id).write_text(
        json.dumps([{"page": i + 1, "text": p} for i, p in enumerate(pages)]), encoding="utf-8"
    )
    log.info("manifesto ingested party=%s chars=%d pages=%d", party_id, len(text), len(pages))
    return True


def ingest_all_manifestos() -> dict:
    results = {}
    for source in MANIFESTOS:
        results[source["party_id"]] = download_manifesto(source)
    return results


def available_manifesto_texts() -> list[dict]:
    out = []
    for source in MANIFESTOS:
        path = _text_path(source["party_id"])
        if path.exists():
            out.append({**source, "text": path.read_text(encoding="utf-8")})
    return out


def available_manifesto_pages() -> list[dict]:
    out = []
    for source in MANIFESTOS:
        path = _pages_path(source["party_id"])
        if path.exists():
            pages = json.loads(path.read_text(encoding="utf-8"))
            out.append({**source, "pages": pages})
    return out
