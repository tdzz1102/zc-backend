from requests import Session
from fastapi import APIRouter
from schema.llm import *
from openai import OpenAI
import os
from utils.logging import logger


router = APIRouter()


def get_session():
    s = Session()
    s.trust_env = False
    try:
        yield s
    finally:
        s.close()


@router.get("/models")
def get_model_list() -> list:
    try:
        s = next(get_session())
        res = s.get(f"{os.getenv('LLM_URL')}/models")
        data = res.json()["data"]
        return data
    except Exception as e:
        logger.error(e)


@router.post("/chat")
def make_chat(data: UserMessage):
    client = OpenAI(base_url=os.getenv('LLM_URL'), api_key=os.getenv('API_KEY'))

    completion = client.chat.completions.create(
        model='mistral_7b',
        messages=[
            {"role": "user", "content": data.message},
        ],
        max_tokens=512,
    )

    return {"message": completion.choices[0].message.content}
    