from fastapi import APIRouter, Request
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import PageModel
from repository import StatsRepository
from .jwt_token import decode_token_and_get_user

router = APIRouter()


@router.get('/stats/', response_model=PageModel)
def get_all_pages_stats(request: Request):
    user_id = decode_token_and_get_user(request)
    return StatsRepository.get_all_pages(user_id)


@router.get('/stats/{page_id)', response_model=PageModel)
def get_page_stats(request: Request, page_id):
    user_id = decode_token_and_get_user(request)
    return StatsRepository.get_page(user_id, page_id)
