from app.rag.promise_store import atoms_by_category, category_counts
from app.rag.sources import MANIFESTOS
from app.rag.taxonomy import TAXONOMY

_PARTY_BY_ID = {m["party_id"]: m for m in MANIFESTOS}


def _enrich(atom: dict) -> dict:
    party = _PARTY_BY_ID.get(atom["party_id"], {})
    return {
        **atom,
        "party_name": party.get("party_name", atom["party_id"]),
        "hue": party.get("hue", "#9184d9"),
    }


def list_categories() -> list[dict]:
    counts = category_counts()
    by_category: dict[str, dict] = {cat: {} for cat in TAXONOMY}
    for row in counts:
        by_category.setdefault(row["taxonomy_category"], {})[row["party_id"]] = row["n"]
    return [{"category": cat, "counts_by_party": by_category.get(cat, {})} for cat in TAXONOMY]


def compare_category(category: str) -> dict:
    atoms = atoms_by_category(category)
    by_party: dict[str, list[dict]] = {}
    for atom in atoms:
        by_party.setdefault(atom["party_id"], []).append(_enrich(atom))

    return {
        "category": category,
        "parties": [
            {
                "party_id": pid,
                "party_name": _PARTY_BY_ID.get(pid, {}).get("party_name", pid),
                "hue": _PARTY_BY_ID.get(pid, {}).get("hue", "#9184d9"),
                "promises": promises,
                "quantified_count": sum(1 for p in promises if p["quantified"]),
                "directional_count": sum(1 for p in promises if not p["quantified"]),
            }
            for pid, promises in by_party.items()
        ],
    }
