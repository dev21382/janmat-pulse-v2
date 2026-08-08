from fastapi import APIRouter

from app.electoral.service import get_comparison

router = APIRouter()


@router.get("/electoral/history")
def electoral_history():
    return get_comparison()
