"""Promise-atom extraction: splits manifesto page text into discrete,
numbered commitments instead of fixed-width chunks, per the product spec's
C1. Manifestos consistently number their commitments ("12. We promise to...",
"1. We will introduce...") — this splits on that real structural signal
rather than an arbitrary word count, so each atom is one citable, taggable
commitment with its real page number attached.

Not every manifesto page is a numbered list (intros, section headers), so
pages that don't match the pattern are skipped for atom extraction — they're
still covered by the existing whole-document TF-IDF chat, which doesn't
require this structure.
"""
import re

from app.rag.taxonomy import classify

# Matches "12. We promise..." style markers: digit(s) + period + space + capital
# letter, anchored so it doesn't fire on decimals like "3.5%" or "Rs. 5".
_ATOM_MARKER = re.compile(r"(?:(?<=\s)|^)(\d{1,3})\.\s+(?=[A-Z])")

_QUANTIFIED_RE = re.compile(
    r"\d|per\s?cent|percent|crore|lakh|rupees?|₹|rs\.?\s?\d|by 20\d{2}|within \d+ (day|month|year)",
    re.IGNORECASE,
)

MIN_ATOM_CHARS = 30
MAX_ATOM_CHARS = 600


def extract_atoms(pages: list[dict], party_id: str) -> list[dict]:
    atoms = []
    for page_entry in pages:
        page_num = page_entry["page"]
        text = re.sub(r"\s+", " ", page_entry["text"]).strip()
        if not text:
            continue

        markers = list(_ATOM_MARKER.finditer(text))
        if len(markers) < 2:
            continue  # not a numbered-list page; skip rather than force false structure

        for i, m in enumerate(markers):
            start = m.end()
            end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
            atom_text = text[start:end].strip()
            if not (MIN_ATOM_CHARS <= len(atom_text) <= MAX_ATOM_CHARS):
                continue

            category, matched_keywords = classify(atom_text)
            atoms.append(
                {
                    "party_id": party_id,
                    "page": page_num,
                    "number": m.group(1),
                    "text": atom_text,
                    "taxonomy_category": category,
                    "matched_keywords": matched_keywords,
                    "quantified": bool(_QUANTIFIED_RE.search(atom_text)),
                }
            )
    return atoms
