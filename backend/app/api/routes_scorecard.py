from fastapi import APIRouter

from app.scorecard.service import list_entries, rollup_by_category, status_options

router = APIRouter()


@router.get("/scorecard/entries")
def get_entries(party_id: str | None = None, taxonomy_category: str | None = None):
    return {"entries": list_entries(party_id, taxonomy_category)}


@router.get("/scorecard/rollup")
def get_rollup():
    return {"rollups": rollup_by_category(), "status_options": status_options()}
