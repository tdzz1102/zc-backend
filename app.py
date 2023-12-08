from fastapi import FastAPI
from views.dataset import router as dataset_router
from views.data import router as data_router
from views.lm import router as lm_router


app = FastAPI()
app.include_router(dataset_router, prefix="/dataset")
app.include_router(data_router, prefix="/data")
app.include_router(lm_router, prefix="/lm")


@app.get("/")
def root():
    return {"message": "Hello World"}
