from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


class Permission(BaseModel):
    id: str
    object: str
    created: int
    allow_create_engine: bool
    allow_sampling: bool
    allow_logprobs: bool
    allow_search_indices: bool
    allow_view: bool
    allow_fine_tuning: bool
    organization: str
    group: str
    is_blocking: bool


class ModelInfo(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str
    root: str
    parent: str
    permission: Permission