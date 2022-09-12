from pydantic import BaseModel
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class PageModel(BaseModel):
    page = dict

    class Config():
        orm_mode = True
