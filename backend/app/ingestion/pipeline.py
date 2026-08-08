import logging
import time

from app.db.database import cursor
from app.ingestion.gdelt import fetch_gdelt
from app.ingestion.news import fetch_news
from app.ingestion.reddit import fetch_reddit
from app.ingestion.topics import TOPICS
from app.sentiment.aggregate import recompute_daily_sentiment
from app.sentiment.scorer import score_texts

log = logging.getLogger("ingestion.pipeline")


def _store_items(topic_id: str, source: str, items: list[dict]) -> int:
    if not items:
        return 0

    scored = score_texts([item["title"] for item in items])

    inserted = 0
    now = int(time.time())
    with cursor() as cur:
        for item, (sentiment, method) in zip(items, scored):
            cur.execute(
                """INSERT OR IGNORE INTO opinion_items
                   (topic_id, source, external_id, title, url, created_utc, fetched_utc, score, sentiment, sentiment_method)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    topic_id,
                    source,
                    item["external_id"],
                    item["title"],
                    item.get("url"),
                    item["created_utc"],
                    now,
                    item.get("score"),
                    sentiment,
                    method,
                ),
            )
            inserted += cur.rowcount
    return inserted


def ingest_topic(topic_id: str) -> dict:
    meta = TOPICS[topic_id]
    query = meta["query"]

    reddit_items, reddit_ok = fetch_reddit(query)
    news_items, news_ok = fetch_news(query)
    gdelt_items, gdelt_ok = fetch_gdelt(query)

    reddit_new = _store_items(topic_id, "reddit", reddit_items)
    news_new = _store_items(topic_id, "news", news_items)
    gdelt_new = _store_items(topic_id, "gdelt", gdelt_items)

    recompute_daily_sentiment(topic_id)

    result = {
        "topic_id": topic_id,
        "reddit_ok": reddit_ok,
        "reddit_fetched": len(reddit_items),
        "reddit_new": reddit_new,
        "news_ok": news_ok,
        "news_fetched": len(news_items),
        "news_new": news_new,
        "gdelt_ok": gdelt_ok,
        "gdelt_fetched": len(gdelt_items),
        "gdelt_new": gdelt_new,
    }
    log.info("ingested topic=%s %s", topic_id, result)
    return result


def ingest_all() -> list[dict]:
    return [ingest_topic(t) for t in TOPICS]
