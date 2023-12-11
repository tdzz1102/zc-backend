from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from utils.auth import get_current_user
from utils.db import get_db
from views.llm import get_model_list
from schema.follow import *
from typing import List


router = APIRouter()


@router.post("/", response_model=FollowResponse)
def create_follow(data: FollowRequest, current_user = Depends(get_current_user)):
    '''
    dataset_id or model_name
    '''
    r = next(get_db())
    r.sadd(f"follow:{current_user.username}", f"{data.type.value}:{data.id}")
    return FollowResponse(username=current_user.username, **data.dict())


@router.get("/{username}", response_model=FollowList)
def get_follow(username: str):
    r = next(get_db())
    follows = r.smembers(f"follow:{username}")
    datasets = []
    models = []
    model_list = get_model_list()
    for follow in follows:
        if follow.startswith("dataset:"):
            datasets.append(r.hgetall(follow))
        elif follow.startswith("model:"):
            model_name = follow.split(":")[1]
            for model in model_list:
                if model.id == model_name:
                    models.append(model)
    return FollowList(username=username, datasets=datasets, models=models)
    
    
@router.get("/", response_model=List[FollowList])
def get_all_follow():
    r = next(get_db())
    usernames = r.keys(f"follow:*")
    res = []
    for username in usernames:
        res.append(get_follow(username.split(":")[1]))
    return res