from pydantic import BaseModel


class RatingResult(BaseModel):
    model_name: str
    total: int
    correct: int