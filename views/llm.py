import os

from fastapi import APIRouter
from openai import OpenAI
from typing import List

from schema.llm import *
from utils.logging import logger
from utils.db import get_requests_session

router = APIRouter()


@router.get("/models", response_model=List[ModelInfo])
def get_model_list() -> list:
    '''
    获取模型列表，是[http://111.202.73.146:10510/v1/models](http://111.202.73.146:10510/v1/models)的代理接口
    
    助教提供的api接口文档在[http://111.202.73.146:10510/docs](http://111.202.73.146:10510/docs)，要用国内ip访问
    '''
    try:
        s = next(get_requests_session())
        res = s.get(f"{os.getenv('LLM_URL')}/models")
        data = res.json()["data"]
        return data
    except Exception as e:
        logger.error(e)


@router.post("/chat", response_model=ChatMessage)
def make_chat(data: ChatMessage, model: str = "mistral_7b"):
    '''
    测试大模型输出，前端不需要调用这个接口
    '''
    client = OpenAI(base_url=os.getenv("LLM_URL"),
                    api_key=os.getenv("API_KEY"))

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": data.message},
        ],
        max_tokens=512,
    )

    return ChatMessage(message=completion.choices[0].message.content)
