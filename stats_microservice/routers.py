from fastapi import APIRouter
from schemas import PageModel
from repository import StatsRepository

router = APIRouter()


@router.get('/stats/{user_id}', response_model=PageModel)
def get_all_pages_stats(user_id):
    return StatsRepository.get_all_pages(user_id)


@router.get('/stats/{user_id}/{page_id)', response_model=PageModel)
def get_all_pages_stats(user_id, page_id):
    return StatsRepository.get_page(user_id, page_id)
