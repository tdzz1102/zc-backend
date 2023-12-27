# 客观题自动评分
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from dotenv import load_dotenv

from schema.data import SelectData
from utils.db import get_db
from utils.llm_client import get_llm_select_result
from utils.logging import logger

load_dotenv()


def autorating_worker(data_id: str):
    r = next(get_db())
    select_data = SelectData(**r.hgetall(f"data:{data_id}"))
    models = r.smembers("models")
    for model in models:
        res = get_llm_select_result(model, select_data)
        if res:
            r.incr(f"rating:{model}:{data_id}:correct")
        else:
            r.incr(f"rating:{model}:{data_id}:incorrect")
    return 20231208 # 返回值无所谓，只是为了让 ThreadPoolExecutor.submit() 返回一个 Future 对象
    

def autorating():
    executor = ThreadPoolExecutor(max_workers=5)
    r = next(get_db())
    while True:
        data_ids = r.smembers("autorating")
        n = len(data_ids)
        if n:
            logger.info(f"autorating {n} data...")
        else:
            logger.debug("no data to autorating")
        for i, data_id in enumerate(data_ids):
            feature = executor.submit(autorating_worker, data_id)
            logger.info(f"autorating {i+1}/{n}")
            feature.result()
            r.srem("autorating", data_id)
        sleep(5)
    