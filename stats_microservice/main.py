from fastapi import FastAPI
from subscriber import subscriber
import time


app = FastAPI()


@app.on_event("startup")
def startup_event():
    time.sleep(15)
    subscriber.setup_connection()
