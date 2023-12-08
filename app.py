from fastapi import FastAPI
from views.dataset import router as dataset_router
from views.data import router as data_router
from views.llm import router as lm_router
from logging import getLogger

from utils.db import get_models_name
from utils.load_dataset import load_all_dataset

from dotenv import load_dotenv


app = FastAPI()
app.include_router(dataset_router, prefix="/dataset")
app.include_router(data_router, prefix="/data")
app.include_router(lm_router, prefix="/lm")
logger = getLogger('uvicorn.app')


@app.on_event("startup")
async def startup():
    load_dotenv()
    load_all_dataset()
    get_models_name()
    logger.info("DB initialized")



@app.get("/")
def root():
    return {"message": "Hello World"}
