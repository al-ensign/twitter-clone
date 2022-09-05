from fastapi import APIRouter


router = APIRouter()


@router.get('/stats/', response_model=XX)
async def get_page_stats():
    pass

