import datetime as dt
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Dataset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: dt.datetime = Field(default_factory=dt.datetime.now)
    name: str
    description: str = None