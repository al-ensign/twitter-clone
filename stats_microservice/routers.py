from fastapi import APIRouter, Request
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import PageModel
from repository import dynamo
from jwt_token import decode_token_and_get_user

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix='/api/v1')


@router.get('/stats/', response_model=PageModel)
def get_stats(request: Request):
    user_id = decode_token_and_get_user(request)
    info = dynamo.get_all_pages(user_id=user_id)
    return JSONResponse(jsonable_encoder(info))
