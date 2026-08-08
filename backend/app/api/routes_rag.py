from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.comparison import compare_category, list_categories
from app.rag.pipeline import answer_query, build_index, index_status
from app.rag.taxonomy import TAXONOMY

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@router.get("/rag/status")
def rag_status():
    return index_status()


@router.post("/rag/build")
def rag_build(force: bool = False):
    return build_index(force=force)


@router.post("/rag/query")
def rag_query(req: QueryRequest):
    return answer_query(req.question, top_k=req.top_k)


@router.get("/manifesto/taxonomy")
def get_taxonomy():
    return {"categories": list_categories()}


@router.get("/manifesto/compare/{category}")
def get_comparison(category: str):
    if category not in TAXONOMY:
        raise HTTPException(404, "unknown taxonomy category")
    return compare_category(category)
