from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from schema.data import *
from utils.db import get_db

router = APIRouter()


@router.get("/")
def get_data_list(dataset_id: str = None):
    r = next(get_db())
    keys = r.keys(f"data:*")
    res = []
    for key in keys:
        data = r.hgetall(key)
        if dataset_id and data["dataset_id"] != dataset_id:
            continue
        res.append(data)
    return res


@router.post("/")
def create_data(data: SelectData | QAData):
    r = next(get_db())
    r.hmset(f"data:{data.id}", jsonable_encoder(data, exclude_none=True))
    if data.type == DataType.select:
        r.sadd('autorating', str(data.id))
    return data


@router.get("/{data_id}")
def get_data(data_id: str):
    r = next(get_db())
    return r.hgetall(f"data:{data_id}")
    
    
@router.delete("/{data_id}")
def delete_data(data_id: str):
    r = next(get_db())
    res = r.delete(f"data:{data_id}")
    return {"status": "ok" if res else "error"}

@router.patch("/{data_id}")
def update_data(data_id: str, data: SelectData | QAData):
    r = next(get_db())
    r.hmset(f"data:{data_id}", jsonable_encoder(data, exclude_none=True))
    if data.type == DataType.select:
        r.sadd('autorating', str(data.id))
    return data