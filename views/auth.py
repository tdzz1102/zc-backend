import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.logging import logger
from utils.db import get_requests_session, get_db
from schema.auth import *


router = APIRouter()


@router.post("/token", response_model=Token)
def get_model_list(user: UserLogin):
    '''
    返回体里有access和refresh两个token，access用于访问需要认证的接口，refresh用于刷新access
    
    但是暂时还没做刷新access的接口，需要刷新的时候重新登录一下就行
    '''
    try:
        s = next(get_requests_session())
        res = s.post(f"{os.getenv('USERS_URL')}/token/", json=user.dict())
        data = res.json()
        if res.status_code == 200:
            r = next(get_db())
            r.hset(f"auth", data["access"], user.username)
        return JSONResponse(content=data, status_code=res.status_code)
    except Exception as e:
        logger.error(e)
