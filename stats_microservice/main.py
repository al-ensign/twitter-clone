import os
import sys

import uvicorn

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from routers import router


app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, port=8001, host='0.0.0.0')


