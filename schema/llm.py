from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


class ModelInfo(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str
    root: str