from pydantic import BaseModel
from enum import Enum


class UserMessage(BaseModel):
    message: str
