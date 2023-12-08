import redis
from requests import Session
import os


def get_db():
    r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
    try:
        yield r
    finally:
        r.close()
        

def get_requests_session():
    s = Session()
    s.trust_env = False
    try:
        yield s
    finally:
        s.close()


def dataset_exists(name: str):
    r = next(get_db())
    keys = r.keys("dataset:*")
    res = []
    for key in keys:
        d = r.hgetall(key)
        if d["name"] == name:
            return True
    return False


def get_models_name():
    r = next(get_db())
    s = next(get_requests_session())
    res = s.get(f"{os.getenv('LLM_URL')}/models")
    data = res.json()["data"]
    for model in data:
        r.sadd("models", model["id"])