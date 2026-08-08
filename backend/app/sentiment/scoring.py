"""Composite scoring methodology for the sentiment dashboard.

Published openly and applied identically to every topic — the PRD's
"equal-treatment protocol" (same methodology, same thresholds, same review
process, no exceptions per topic/party) is implemented here as literal code
uniformity: every topic goes through this exact function, no special cases.

Score bands and confidence thresholds match the PRD's Pillar A9 spec
verbatim so the legend shown in the UI is the actual methodology, not a
simplified gloss of it.
"""
from app.db.database import cursor

SCORE_BANDS = [
    (60, 100, "Strongly Positive"),
    (20, 59, "Positive"),
    (-19, 19, "Neutral / Mixed"),
    (-59, -20, "Negative"),
    (-100, -60, "Strongly Negative"),
]

# PRD-specified thresholds. Our actual per-topic daily volume (News RSS only,
# Reddit blocked from most cloud networks) rarely reaches even the "Medium"
# band — that is the honest point of showing it: a thin-data topic should
# never look as authoritative as a heavily tracked one, even inside a demo.
CONFIDENCE_THRESHOLDS = [
    (5000, "High"),
    (500, "Medium"),
    (0, "Low"),
]


def band_for_score(score_100: float) -> str:
    for lo, hi, label in SCORE_BANDS:
        if lo <= score_100 <= hi:
            return label
    return "Neutral / Mixed"


def confidence_for_count(item_count: int) -> str:
    for threshold, label in CONFIDENCE_THRESHOLDS:
        if item_count >= threshold:
            return label
    return "Low"


def composite_summary(topic_id: str, window_days: int = 7) -> dict:
    with cursor() as cur:
        cur.execute(
            """SELECT mean_sentiment, item_count FROM daily_sentiment
               WHERE topic_id=? ORDER BY day DESC LIMIT ?""",
            (topic_id, window_days),
        )
        rows = cur.fetchall()

    if not rows:
        return {
            "topic_id": topic_id,
            "score_100": 0,
            "band": band_for_score(0),
            "item_count": 0,
            "confidence": confidence_for_count(0),
            "window_days": window_days,
            "positive_share": None,
            "neutral_share": None,
            "negative_share": None,
        }

    total_items = sum(r["item_count"] for r in rows)
    weighted = sum(r["mean_sentiment"] * r["item_count"] for r in rows)
    mean_sentiment = weighted / total_items if total_items else 0.0
    score_100 = round(mean_sentiment * 100, 1)

    with cursor() as cur:
        cur.execute(
            """SELECT sentiment FROM opinion_items
               WHERE topic_id=? AND sentiment IS NOT NULL
               ORDER BY created_utc DESC LIMIT 500""",
            (topic_id,),
        )
        sentiments = [r["sentiment"] for r in cur.fetchall()]

    pos = sum(1 for s in sentiments if s > 0.05)
    neg = sum(1 for s in sentiments if s < -0.05)
    neu = len(sentiments) - pos - neg
    n = len(sentiments) or 1

    return {
        "topic_id": topic_id,
        "score_100": score_100,
        "band": band_for_score(score_100),
        "item_count": total_items,
        "confidence": confidence_for_count(total_items),
        "window_days": window_days,
        "positive_share": round(pos / n, 3),
        "neutral_share": round(neu / n, 3),
        "negative_share": round(neg / n, 3),
    }


def legend() -> list[dict]:
    return [{"min": lo, "max": hi, "label": label} for lo, hi, label in SCORE_BANDS]
