import datetime as dt

from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from enum import Enum


class DataType(str, Enum):
    select = "select"
    qa = "qa"
    

class BaseData(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: dt.datetime = dt.datetime.now()
    dataset_id: str
    type: DataType
    question: str
    subject: str = None


class SelectData(BaseData):
    A: str
    B: str
    C: str
    D: str
    answer: int
    
    
class QAData(BaseData):
    answer: str = None
    answer_GPT35: str
    answer_GPT4: str