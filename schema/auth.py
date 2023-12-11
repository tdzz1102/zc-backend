from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserLogin(User):
    password: str

class Token(BaseModel):
    access: str
    refresh: str
