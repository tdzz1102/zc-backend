import uvicorn
import threading

from fastapi import FastAPI
from views.dataset import router as dataset_router
from views.data import router as data_router
from views.llm import router as llm_router
from views.rating import router as rating_router
from utils.db import get_models_name
from utils.load_dataset import load_all_dataset
from dotenv import load_dotenv
from utils.auto_rating import autorating
from utils.logging import logger


app = FastAPI()
app.include_router(dataset_router, prefix="/dataset")
app.include_router(data_router, prefix="/data")
app.include_router(llm_router, prefix="/llm")
app.include_router(rating_router, prefix="/rating")


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
    uvicorn.run('app:app', host="0.0.0.0")
