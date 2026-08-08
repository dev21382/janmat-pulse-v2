"""LLM-based taxonomy classification for promise-atoms, via the same free
Groq key already used for generative RAG answers. This is the real
"ML-driven" classification tier — keyword matching (taxonomy.py) is kept
purely as the offline fallback when no key is configured or a batch call
fails, and every atom is tagged with which method actually classified it.
"""
import json
import logging
import re

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.rag.taxonomy import TAXONOMY

log = logging.getLogger("rag.llm_taxonomy")

BATCH_SIZE = 20

_SYSTEM_PROMPT = (
    "You classify Indian political manifesto commitments into exactly one of these 10 "
    "categories:\n" + "\n".join(f"{i + 1}. {c}" for i, c in enumerate(TAXONOMY)) + "\n\n"
    "You will receive a numbered list of promise texts. Respond with ONLY a JSON array of "
    "category name strings, one per input, in the same order, using the exact category names "
    "given above. No explanation, no markdown, just the JSON array."
)

_JSON_ARRAY_RE = re.compile(r"\[.*\]", re.DOTALL)


def available() -> bool:
    return bool(GROQ_API_KEY)


def _classify_one_batch(texts: list[str]) -> list[str] | None:
    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        numbered = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(texts))
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": numbered},
            ],
            temperature=0,
            max_tokens=2000,
        )
        raw = completion.choices[0].message.content or ""
        match = _JSON_ARRAY_RE.search(raw)
        if not match:
            log.warning("llm taxonomy: no JSON array in response: %s", raw[:200])
            return None
        parsed = json.loads(match.group(0))
    except Exception as exc:
        log.warning("llm taxonomy batch failed: %s", exc)
        return None

    if not isinstance(parsed, list) or len(parsed) != len(texts):
        log.warning("llm taxonomy: response length mismatch (%d vs %d)", len(parsed) if isinstance(parsed, list) else -1, len(texts))
        return None

    valid = []
    for category in parsed:
        if category not in TAXONOMY:
            log.warning("llm taxonomy: invalid category returned: %r", category)
            return None
        valid.append(category)
    return valid


def classify_batch(atoms: list[dict]) -> list[dict]:
    """Mutates and returns atoms in place: sets taxonomy_category + taxonomy_method
    for every atom the LLM successfully classifies, one batch at a time, leaving
    the pre-computed keyword classification untouched wherever the LLM path fails."""
    if not available():
        return atoms

    for i in range(0, len(atoms), BATCH_SIZE):
        batch = atoms[i : i + BATCH_SIZE]
        categories = _classify_one_batch([a["text"] for a in batch])
        if categories is None:
            continue
        for atom, category in zip(batch, categories):
            atom["taxonomy_category"] = category
            atom["taxonomy_method"] = "llm"

    return atoms
