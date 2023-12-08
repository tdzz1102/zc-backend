from uuid import uuid4, UUID
import datetime as dt
from pydantic import BaseModel, Field


class Dataset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: dt.datetime = dt.datetime.now()
    name: str
    description: str = None