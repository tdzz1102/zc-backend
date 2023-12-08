import uvicorn
import threading

from fastapi import FastAPI
from views.dataset import router as dataset_router
from views.data import router as data_router
from views.llm import router as llm_router
from views.rating import router as rating_router
from logging import getLogger
from utils.db import get_models_name
from utils.load_dataset import load_all_dataset
from dotenv import load_dotenv
from uvicorn.config import LOGGING_CONFIG
from utils.auto_rating import autorating


app = FastAPI()
app.include_router(dataset_router, prefix="/dataset")
app.include_router(data_router, prefix="/data")
app.include_router(llm_router, prefix="/llm")
app.include_router(rating_router, prefix="/rating")

logger = getLogger('uvicorn.app')
logger.setLevel("DEBUG")
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"


@app.on_event("startup")
async def startup():
    load_dotenv()
    load_all_dataset()
    get_models_name()
    logger.info("DB initialized")


@app.get("/")
def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    thread = threading.Thread(target=autorating, daemon=True)
    thread.start()
    uvicorn.run('app:app')
