from pydantic import BaseModel
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class PageModel(BaseModel):
    user_id: int
    page_id: int
    followers: int
    follow_requests: int
    tweets: int
    likes: int
    is_blocked: bool
    status: str

    class Config():
        orm_mode = True
