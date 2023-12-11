import datetime as dt
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DataType(str, Enum):
    select = "select"
    qa = "qa"
    

class BaseData(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    dataset_id: UUID
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
    answer_GPT35: str = None
    answer_GPT4: str = None