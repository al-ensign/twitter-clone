import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from database import initialize_db


app = FastAPI()

db = initialize_db()


