from app.scorecard.seed_data import SCORECARD_ENTRIES, STATUS_OPTIONS


def list_entries(party_id: str | None = None, taxonomy_category: str | None = None) -> list[dict]:
    entries = SCORECARD_ENTRIES
    if party_id:
        entries = [e for e in entries if e["party_id"] == party_id]
    if taxonomy_category:
        entries = [e for e in entries if e["taxonomy_category"] == taxonomy_category]
    return entries


def rollup_by_category() -> list[dict]:
    """Top-10-subsection rollup per party, per D3 — always with drill-down to
    the individual entries behind it, never a bare headline number."""
    by_category: dict[str, list[dict]] = {}
    for e in SCORECARD_ENTRIES:
        by_category.setdefault(e["taxonomy_category"], []).append(e)

    rollups = []
    for category, entries in by_category.items():
        delivery_indices = [e["delivery_index"] for e in entries if e["delivery_index"] is not None]
        rollups.append(
            {
                "taxonomy_category": category,
                "entry_count": len(entries),
                "avg_delivery_index": round(sum(delivery_indices) / len(delivery_indices), 3)
                if delivery_indices
                else None,
                "status_breakdown": {
                    status: sum(1 for e in entries if e["status"] == status) for status in STATUS_OPTIONS
                },
                "entries": entries,
            }
        )
    return rollups


def status_options() -> list[str]:
    return STATUS_OPTIONS
