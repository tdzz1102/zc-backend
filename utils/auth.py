from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.db import get_db
from schema.auth import User
import os


security = HTTPBearer()


def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)) -> User:
    if authorization.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    r = next(get_db())
    username = r.hget(f"auth", authorization.credentials)
    if username:
        return User(username=username)
    if os.getenv("AUTHENTICATION") == "0": # for debug
        return User(username="admin")
    raise HTTPException(status_code=401, detail="Invalid token")
