"""GDELT DOC 2.0 API ingestion — free, no API key. Per the product spec this
is "the highest-value free source" and was the one concrete recommendation
from that document this project hadn't actually wired up; Google News RSS
alone was leaving it on the table.

GDELT does rate-limit — its exact bucket isn't publicly documented, but
observed 429s persisted even ~15s apart during testing — so this module
self-throttles to roughly one request per 6 seconds and retries once after
a 10s backoff on a 429, rather than firing all topic queries as fast as the
ingestion loop can issue them. Even so, occasional 429s are expected and
handled the same way as any other source outage: the topic just falls back
to whichever sources did succeed that cycle, and GDELT catches up on the
next hourly run.
"""
import logging
import threading
import time
from datetime import datetime, timezone
from typing import TypedDict

import httpx

log = logging.getLogger("ingestion.gdelt")

DOC_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
MIN_INTERVAL_SECONDS = 6.0

_HEADERS = {"User-Agent": "python:janmat-pulse-v2:v1.0 (public-interest news ingestion; contact via GitHub)"}

_lock = threading.Lock()
_last_request_at = 0.0


class GdeltItem(TypedDict):
    external_id: str
    title: str
    url: str
    created_utc: int


def _parse_seendate(raw: str) -> int:
    try:
        return int(datetime.strptime(raw, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).timestamp())
    except Exception:
        return int(time.time())


def _throttle() -> None:
    global _last_request_at
    with _lock:
        wait = MIN_INTERVAL_SECONDS - (time.monotonic() - _last_request_at)
        if wait > 0:
            time.sleep(wait)
        _last_request_at = time.monotonic()


def _request(params: dict) -> httpx.Response | None:
    _throttle()
    try:
        return httpx.get(DOC_API_URL, params=params, headers=_HEADERS, timeout=15.0)
    except Exception as exc:
        log.warning("gdelt request failed: %s", exc)
        return None


def fetch_gdelt(query: str, limit: int = 50) -> tuple[list[GdeltItem], bool]:
    params = {
        "query": f"{query} sourcelang:english",
        "mode": "artlist",
        "maxrecords": str(limit),
        "sort": "DateDesc",
        "format": "json",
    }

    resp = _request(params)
    if resp is not None and resp.status_code == 429:
        log.info("gdelt rate-limited, backing off 10s and retrying once")
        time.sleep(10.0)
        resp = _request(params)

    if resp is None:
        return [], False
    if resp.status_code != 200:
        log.warning("gdelt fetch non-200 status=%s query=%r", resp.status_code, query)
        return [], False

    try:
        payload = resp.json()
    except Exception as exc:
        log.warning("gdelt response not JSON query=%r err=%s", query, exc)
        return [], False

    items: list[GdeltItem] = []
    for article in payload.get("articles", []):
        url = article.get("url")
        title = article.get("title")
        if not url or not title:
            continue
        items.append(
            GdeltItem(
                external_id=str(hash(url)),
                title=title,
                url=url,
                created_utc=_parse_seendate(article.get("seendate", "")),
            )
        )
    return items, True
