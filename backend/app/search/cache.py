"""Strictly size-bounded, short-TTL in-process cache for ad-hoc search
results, per the product spec's explicit warning that an unbounded cache is
the most common way a free-tier service quietly climbs past its memory
ceiling. Hard maxsize, oldest-first eviction — deliberately simpler than a
true LRU, matching what the spec actually asks for.
"""
import time
from collections import OrderedDict
from threading import Lock

MAX_ENTRIES = 200
TTL_SECONDS = 15 * 60

_store: "OrderedDict[str, tuple[float, dict]]" = OrderedDict()
_lock = Lock()


def get(key: str) -> dict | None:
    with _lock:
        entry = _store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if time.monotonic() > expires_at:
            del _store[key]
            return None
        return value


def set(key: str, value: dict) -> None:
    with _lock:
        _store[key] = (time.monotonic() + TTL_SECONDS, value)
        _store.move_to_end(key)
        while len(_store) > MAX_ENTRIES:
            _store.popitem(last=False)
