from pydantic import BaseModel
from schema.dataset import Dataset
from schema.llm import ModelInfo
from typing import List
from enum import Enum


class FollowType(str, Enum):
    dataset = "dataset"
    model = "model"
    
    
class FollowRequest(BaseModel):
    type: FollowType
    id: str # dataset_id or model_name
    

class FollowResponse(FollowRequest):
    username: str
    

class FollowList(BaseModel):
    username: str
    datasets: List[Dataset]
    models: List[ModelInfo]