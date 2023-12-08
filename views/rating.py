from fastapi import APIRouter
from utils.db import get_db
from schema.rating import *


router = APIRouter()


# @router.get("/result")
# def get_result():
#     r = next(get_db())
#     res = db["rating"].find_one({"_id": "result"})
#     return res