import logging

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.sentiment.hf_classifier import available as hf_available
from app.sentiment.hf_classifier import classify_batch

log = logging.getLogger("sentiment.scorer")

_analyzer = SentimentIntensityAnalyzer()


def score_text(text: str) -> float:
    """Returns VADER compound sentiment score in [-1, 1]. Single-item path,
    used only where batching isn't available (e.g. an ad-hoc query)."""
    return _analyzer.polarity_scores(text)["compound"]


def method_in_use() -> str:
    return "hf_roberta" if hf_available() else "vader"


def score_texts(texts: list[str]) -> list[tuple[float, str]]:
    """Batch-scores texts, preferring the real ML classifier (HF Inference
    API) when configured, filling any gap (no token, or the batch call
    failed) with VADER — every score is tagged with which method actually
    produced it, never silently blended as if they were the same thing."""
    if not texts:
        return []

    hf_scores = classify_batch(texts)
    if hf_scores is not None:
        return [(s, "hf_roberta") for s in hf_scores]

    log.info("HF classifier unavailable for this batch, falling back to VADER (n=%d)", len(texts))
    return [(score_text(t), "vader") for t in texts]
