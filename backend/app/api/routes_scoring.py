from fastapi import APIRouter, HTTPException

from app.ingestion.topics import TOPICS
from app.sentiment.scoring import composite_summary, legend

router = APIRouter()


@router.get("/scoring/legend")
def get_legend():
    return {"bands": legend(), "confidence_thresholds": {"high": 5000, "medium": 500}}


@router.get("/scoring/summary/{topic_id}")
def get_summary(topic_id: str, window_days: int = 7):
    if topic_id not in TOPICS:
        raise HTTPException(404, "unknown topic")
    return composite_summary(topic_id, window_days=window_days)
