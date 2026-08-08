from fastapi import APIRouter, HTTPException

from app.search.service import search

router = APIRouter()


@router.get("/search")
def search_route(q: str):
    q = q.strip()
    if not q:
        raise HTTPException(400, "query parameter 'q' is required")
    if len(q) > 200:
        raise HTTPException(400, "query too long")
    return search(q)
