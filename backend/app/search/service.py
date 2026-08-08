"""On-demand free-text search (product spec A8 + A10): expands the query,
fans out to sources concurrently with a per-source timeout budget so one
slow source never blocks the whole response, scores sentiment, and builds
an evidence panel of the top-2-by-reach items per sentiment bucket.

GDELT is deliberately excluded from this live path — it self-throttles to
one request per ~6s (see ingestion/gdelt.py) and shares that limiter with
the scheduled ingestion job, which would make an interactive search wait on
a global lock. It stays a background-ingestion-only source; live search
covers Reddit + Google News, both of which respond in low single-digit
seconds.

Reach (A10) is computed honestly rather than uniformly: Reddit items have a
real engagement number (score/upvotes), so their reach is a genuine
percentile within the result set. News items have no engagement metric at
all, so their reach is a recency percentile instead — clearly labeled as
such rather than presented as equivalent to real engagement.
"""
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

from app.ingestion.news import fetch_news
from app.ingestion.reddit import fetch_reddit
from app.search.cache import get as cache_get
from app.search.cache import set as cache_set
from app.search.query_expansion import expand_query
from app.sentiment.scorer import score_texts
from app.sentiment.scoring import band_for_score, confidence_for_count

log = logging.getLogger("search.service")

SOURCE_TIMEOUT_SECONDS = 8.0
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="search")


def _resolve_with_budget(future, name: str):
    try:
        return future.result(timeout=SOURCE_TIMEOUT_SECONDS)
    except FutureTimeoutError:
        log.warning("source fetch exceeded %ss budget: %s", SOURCE_TIMEOUT_SECONDS, name)
        return [], False
    except Exception as exc:
        log.warning("source fetch failed: %s err=%s", name, exc)
        return [], False


def _percentile_ranks(values: list[float]) -> list[float]:
    if not values:
        return []
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    n = len(values)
    for rank, idx in enumerate(order):
        ranks[idx] = rank / max(n - 1, 1)
    return ranks


def _bucket(sentiment: float) -> str:
    if sentiment > 0.05:
        return "positive"
    if sentiment < -0.05:
        return "negative"
    return "neutral"


def search(query: str, use_cache: bool = True) -> dict:
    cache_key = query.strip().lower()
    if use_cache:
        cached = cache_get(cache_key)
        if cached is not None:
            return {**cached, "cache_hit": True}

    expanded = expand_query(query)

    reddit_future = _executor.submit(fetch_reddit, expanded)
    news_future = _executor.submit(fetch_news, expanded)
    reddit_items, reddit_ok = _resolve_with_budget(reddit_future, "reddit")
    news_items, news_ok = _resolve_with_budget(news_future, "news")

    all_items = [{**item, "source": "reddit"} for item in reddit_items] + [
        {**item, "source": "news"} for item in news_items
    ]

    if not all_items:
        result = {
            "query": query,
            "expanded_query": expanded,
            "reddit_ok": reddit_ok,
            "news_ok": news_ok,
            "item_count": 0,
            "score_100": 0,
            "band": band_for_score(0),
            "confidence": confidence_for_count(0),
            "evidence": {"positive": [], "neutral": [], "negative": []},
            "items": [],
        }
        return result

    scored = score_texts([item["title"] for item in all_items])
    for item, (sentiment, method) in zip(all_items, scored):
        item["sentiment"] = sentiment
        item["sentiment_method"] = method
        item["bucket"] = _bucket(sentiment)

    reddit_scores = [i["score"] for i in all_items if i["source"] == "reddit"]
    reddit_reach = iter(_percentile_ranks(reddit_scores))
    news_created = [i["created_utc"] for i in all_items if i["source"] == "news"]
    news_reach = iter(_percentile_ranks(news_created))

    for item in all_items:
        if item["source"] == "reddit":
            item["reach_percentile"] = round(next(reddit_reach), 3)
            item["reach_basis"] = "engagement"
        else:
            item["reach_percentile"] = round(next(news_reach), 3)
            item["reach_basis"] = "recency"

    mean_sentiment = sum(i["sentiment"] for i in all_items) / len(all_items)
    score_100 = round(mean_sentiment * 100, 1)

    evidence = {"positive": [], "neutral": [], "negative": []}
    for bucket in evidence:
        bucket_items = sorted(
            (i for i in all_items if i["bucket"] == bucket),
            key=lambda i: i["reach_percentile"],
            reverse=True,
        )
        evidence[bucket] = bucket_items[:2]

    result = {
        "query": query,
        "expanded_query": expanded,
        "reddit_ok": reddit_ok,
        "news_ok": news_ok,
        "item_count": len(all_items),
        "score_100": score_100,
        "band": band_for_score(score_100),
        "confidence": confidence_for_count(len(all_items)),
        "evidence": evidence,
        "items": sorted(all_items, key=lambda i: i["created_utc"], reverse=True)[:50],
        "cache_hit": False,
        "generated_at": int(time.time()),
    }

    if use_cache:
        cache_set(cache_key, result)

    return result
