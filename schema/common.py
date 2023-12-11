from pydantic import BaseModel


class CommonStatus(BaseModel):
    status: str