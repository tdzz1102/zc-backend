import redis


def get_db():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    try:
        yield r
    finally:
        r.close()


def dataset_exists(name: str):
    r = next(get_db())
    keys = r.keys("dataset:*")
    res = []
    for key in keys:
        d = r.hgetall(key)
        if d["name"] == name:
            return True
    return False