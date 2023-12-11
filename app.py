import threading

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends

from utils.auto_rating import autorating
from utils.db import get_models_name
from utils.load_dataset import load_all_dataset
from utils.logging import logger
from utils.auth import get_current_user
from views.data import router as data_router
from views.dataset import router as dataset_router
from views.llm import router as llm_router
from views.rating import router as rating_router
from views.auth import router as auth_router
from schema.auth import User
from schema.common import *


app = FastAPI()
app.include_router(dataset_router, prefix="/dataset")
app.include_router(data_router, prefix="/data")
app.include_router(llm_router, prefix="/llm")
app.include_router(rating_router, prefix="/rating")
app.include_router(auth_router, prefix="/auth")


@app.on_event("startup")
async def startup():
    load_dotenv()
    load_all_dataset()
    get_models_name()
    logger.info("DB initialized")


@app.get("/", response_model=CommonStatus)
def root():
    return CommonStatus(status="Hello, world!")

@app.get("/whoami", response_model=User)
def get_user(user = Depends(get_current_user)):
    return user


if __name__ == "__main__":
    thread = threading.Thread(target=autorating, daemon=True)
    thread.start()
    uvicorn.run('app:app', host="0.0.0.0", reload=True)
