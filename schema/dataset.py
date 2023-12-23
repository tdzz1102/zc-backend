import datetime as dt
from uuid import UUID, uuid4
from schema.common import *
from schema.data import DataType

from pydantic import BaseModel, Field


class DatasetCreate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    description: str = None
    name: str
    type: DataType = DataType.select
    

class Dataset(DatasetCreate):
    created_by: str = 'admin'