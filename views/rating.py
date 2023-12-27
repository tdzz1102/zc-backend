import random

from fastapi import APIRouter, Depends

from schema.rating import *
from utils.db import get_db
from utils.llm_client import get_llm_response
from utils.auth import get_current_user

router = APIRouter()


@router.get("/result", response_model=list[RatingResult])
def get_result(sort_by: str = "correct_rate"):
    r = next(get_db())
    models = r.smembers("models")
    datasets = r.keys("dataset:*")

    res = {}

    for dataset_key in datasets:
        dataset_id = dataset_key.split(":")[-1]
        datasets = r.keys("dataset:*")  # 假设数据集键以 "dataset:" 开头

    res = []

    for dataset_key in datasets:
        dataset_id = dataset_key.split(":")[-1]

        for model in models:
            rating_result = RatingResult(
                model_name=model,
                dataset_id=dataset_id,
                correct=int(r.get(f"rating:{model}:{dataset_id}:correct") or 0),
                incorrect=int(r.get(f"rating:{model}:{dataset_id}:incorrect") or 0),
                good=int(r.get(f"rating:{model}:{dataset_id}:good") or 0),
                soso=int(r.get(f"rating:{model}:{dataset_id}:soso") or 0),
                bad=int(r.get(f"rating:{model}:{dataset_id}:bad") or 0),
                win=int(r.get(f"rating:{model}:{dataset_id}:win") or 0),
                lose=int(r.get(f"rating:{model}:{dataset_id}:lose") or 0),
                correct_rate=float(r.get(f"rating:{model}:{dataset_id}:correct_rate") or 0.0),
                subjective_score=float(r.get(f"rating:{model}:{dataset_id}:subjective_score") or 0.0),
                win_rate=float(r.get(f"rating:{model}:{dataset_id}:win_rate") or 0.0),
            )

            res.append(rating_result)

    if sort_by and hasattr(res[-1], sort_by):
        res.sort(key=lambda x: getattr(x, sort_by), reverse=True)

    return res


@router.get("/subjective", response_model=SubjectiveQuestion)
def get_subjective_rating_question():
    '''
    获取主观题评分题目
    '''
    r = next(get_db())
    keys = r.keys("data:*")
    while True:
        key = random.choice(keys)
        if r.hget(key, "type") == "qa":
            break
    models = list(r.smembers("models"))
    model = random.choice(models)
    answer = get_llm_response(model, r.hget(key, "question"))
    return SubjectiveQuestion(
        question_data=QAData(**r.hgetall(key)),
        answer=ModelAnswer(model_name=model, answer=answer)
    )
    

@router.post("/subjective", response_model=CommonStatus)
def submit_subjective_rating_result(subjective_result: SubjectiveResult, current_user = Depends(get_current_user)):
    '''
    提交主观题评分结果
    '''
    r = next(get_db())
    models = r.smembers("models")
    datasets = r.keys("dataset:*")
    if subjective_result.model_name not in models:
        return CommonStatus(message="invalid model")
    if f"dataset:{subjective_result.dataset_id}" not in datasets:
        return CommonStatus(message="invalid dataset")
    r.incr(f"rating:{subjective_result.model_name}:{subjective_result.dataset_id}:{subjective_result.evaluation.value}")

    return CommonStatus(status="ok")
    

@router.get("/competitive", response_model=CompetitiveQuestion)
def get_competitive_rating_question():
    '''
    获取对抗评分题目
    '''
    r = next(get_db())
    keys = r.keys("data:*")
    while True:
        key = random.choice(keys)
        if r.hget(key, "type") == "qa":
            break
    models = list(r.smembers("models"))
    model1, model2 = random.sample(models, 2)
    answer1, answer2 = get_llm_response(model1, r.hget(key, "question")), get_llm_response(model2, r.hget(key, "question"))
    return CompetitiveQuestion(
        question_data=QAData(**r.hgetall(key)),
        answer1=ModelAnswer(model_name=model1, answer=answer1),
        answer2=ModelAnswer(model_name=model2, answer=answer2)
    )


@router.post("/competitive", response_model=CommonStatus)
def submit_competitive_rating_result(competitive_result: CompetitiveResult, current_user = Depends(get_current_user)):
    '''
    提交对抗评分结果
    '''
    r = next(get_db())
    models = r.smembers("models")
    datasets = r.keys("dataset:*")
    if competitive_result.winner not in models \
        or competitive_result.loser not in models \
        or competitive_result.winner == competitive_result.loser:
        return CommonStatus(message="invalid result")
    if f"dataset:{competitive_result.dataset_id}" not in datasets:
        return CommonStatus(message="invalid dataset")
    r.incr(f"rating:{competitive_result.winner}:{competitive_result.dataset_id}:win")
    r.incr(f"rating:{competitive_result.loser}:{competitive_result.dataset_id}:lose")

    return CommonStatus(status="ok")
    