import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from database import initialize_db
from subscriber import subscriber
import time


app = FastAPI()


db = initialize_db()


@app.on_event("startup")
def startup_event():
    time.sleep(15)
    subscriber.setup_connection()
