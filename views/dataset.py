import datetime as dt

from fastapi import APIRouter
from utils.db import get_db
from schema.dataset import *
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.get("/")
def get_dataset_list():
    r = next(get_db())
    keys = r.keys("dataset:*")
    res = []
    for key in keys:
        res.append(r.hgetall(key))
    return res


@router.post("/")
def create_dataset(dataset: Dataset):
    r = next(get_db())
    r.hmset(f"dataset:{dataset.id}", jsonable_encoder(dataset, exclude_none=True))
    return dataset


@router.get("/{dataset_id}")
def get_dataset(dataset_id: str):
    r = next(get_db())
    return r.hgetall(f"dataset:{dataset_id}")


@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: str):
    r = next(get_db())
    res = r.delete(f"dataset:{dataset_id}")
    return {"status": "ok" if res else "error"}


@router.patch("/{dataset_id}")
def update_dataset(dataset_id: str, dataset: Dataset):
    r = next(get_db())
    r.hmset(f"dataset:{dataset_id}", jsonable_encoder(dataset, exclude_none=True))
    return dataset