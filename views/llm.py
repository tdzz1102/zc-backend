from requests import Session
from fastapi import APIRouter
from schema.llm import *
from openai import OpenAI
from utils.db import get_db
import os


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
    s = next(get_session())
    res = s.get(f"{os.getenv('LLM_URL')}/models")
    data = res.json()["data"]
    return data


@router.post("/chat")
def make_chat(data: UserMessage):
    client = OpenAI(base_url=os.getenv('LLM_URL'), api_key="sk-5b9b7b0b-5b7e-4b7e-8b9b-7b0b5b7e4b7e")

    completion = client.chat.completions.create(
        model='mistral_7b',
        messages=[
            {"role": "user", "content": data.message},
        ],
        max_tokens=512,
    )

    return {"message": completion.choices[0].message.content}
    