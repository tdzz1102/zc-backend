import os

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from openai import OpenAI
from typing import List
import json

from schema.llm import *
from utils.logging import logger
from utils.db import get_requests_session
from utils.load_dataset import get_data_path

router = APIRouter()


@router.get("/model", response_model=List[ModelInfo])
def get_model_list():
    '''
    获取模型列表，是[http://111.202.73.146:10510/v1/models](http://111.202.73.146:10510/v1/models)的代理接口
    
    助教提供的api接口文档在[http://111.202.73.146:10510/docs](http://111.202.73.146:10510/docs)，要用国内ip访问
    '''
    model_list = json.load(get_data_path("model_list.json").open())['data']
    res = []
    for model in model_list:
        res.append(ModelInfo(**model))
    return res


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
