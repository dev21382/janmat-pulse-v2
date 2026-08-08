"""Real transformer-based sentiment classification via Hugging Face's free
Inference API, per the product spec's own recommendation for free-tier
deployment (call out to hosted inference rather than loading model weights
in-process, which doesn't fit a 512MB budget alongside a live web server).

Model: cardiffnlp/twitter-roberta-base-sentiment-latest — a RoBERTa model
fine-tuned on ~124M tweets for 3-class sentiment (positive/neutral/negative),
a genuine supervised ML classifier, not a rule-based scorer like VADER.

Requires HF_API_TOKEN (free, from huggingface.co/settings/tokens). Without
it, or on any API failure (cold-start 503, rate limit, network error), the
caller falls back to VADER — this module never raises, it returns None to
signal "use the fallback" so that failure mode is always explicit.
"""
import logging
import os

import httpx

log = logging.getLogger("sentiment.hf_classifier")

HF_API_TOKEN = os.environ.get("HF_API_TOKEN", "").strip()
HF_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"


def available() -> bool:
    return bool(HF_API_TOKEN)


def classify_batch(texts: list[str], timeout: float = 20.0) -> list[float] | None:
    """Returns a list of compound scores in [-1, 1] (P(positive) - P(negative)),
    one per input text, or None if the whole batch should fall back to VADER."""
    if not HF_API_TOKEN or not texts:
        return None

    try:
        resp = httpx.post(
            HF_URL,
            headers={"Authorization": f"Bearer {HF_API_TOKEN}"},
            json={"inputs": texts, "options": {"wait_for_model": True}},
            timeout=timeout,
        )
        if resp.status_code != 200:
            log.warning("HF inference non-200 status=%s body=%s", resp.status_code, resp.text[:200])
            return None
        results = resp.json()
    except Exception as exc:
        log.warning("HF inference call failed: %s", exc)
        return None

    if not isinstance(results, list) or len(results) != len(texts):
        log.warning("HF inference unexpected response shape: %s", str(results)[:200])
        return None

    scores = []
    for item in results:
        by_label = {row["label"].lower(): row["score"] for row in item}
        pos = by_label.get("positive", 0.0)
        neg = by_label.get("negative", 0.0)
        scores.append(round(pos - neg, 4))
    return scores
