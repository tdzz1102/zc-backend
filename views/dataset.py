from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import os

from schema.dataset import *
from utils.auth import get_current_user
from utils.db import get_db

router = APIRouter()


@router.get("/", response_model=List[Dataset])
def get_dataset_list(contains: str = None):
    r = next(get_db())
    keys = r.keys("dataset:*")
    res = []
    for key in keys:
        title = r.hget(key, "name")
        if contains and contains not in title:
            continue
        res.append(r.hgetall(key))
    return res


@router.post("/", response_model=Dataset)
def create_dataset(dataset_create: DatasetCreate, current_user = Depends(get_current_user)):
    r = next(get_db())
    dataset = Dataset(**dataset_create.dict(), created_by=current_user.username)
    r.hmset(f"dataset:{dataset.id}", jsonable_encoder(dataset, exclude_none=True))
    return dataset


@router.get("/{dataset_id}", response_model=Dataset)
def get_dataset(dataset_id: str):
    r = next(get_db())
    return r.hgetall(f"dataset:{dataset_id}")


@router.delete("/{dataset_id}", response_model=CommonStatus)
def delete_dataset(dataset_id: str, current_user = Depends(get_current_user)):
    r = next(get_db())
    res = r.delete(f"dataset:{dataset_id}")
    return CommonStatus(status="ok" if res else "error")


@router.patch("/{dataset_id}", response_model=Dataset)
def update_dataset(dataset_id: str, dataset: Dataset, current_user = Depends(get_current_user)):
    r = next(get_db())
    r.hmset(f"dataset:{dataset_id}", jsonable_encoder(dataset, exclude_none=True))
    return dataset


@router.post("/upload")
def upload_dataset_file(file: UploadFile = File(...)):
    file_location = f"data/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@router.get("/download/{filename}")
def download_dataset_file(filename: str):
    file_location = f"data/{filename}"
    if os.path.exists(file_location):
        return FileResponse(path=file_location, filename=filename)
    return {"error": "File not found."}
