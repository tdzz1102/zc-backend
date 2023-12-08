import random
from fastapi import APIRouter
from utils.db import get_db
from schema.rating import *
from utils.llm_client import get_llm_response


router = APIRouter()


@router.get("/result", response_model=list[RatingResult])
def get_result(sort_by: str = "correct_rate"):
    r = next(get_db())
    models = r.smembers("models")
    res = []
    for model in models:
        res.append(
            RatingResult(
                model_name=model,
                correct=int(r.get(f"rating:{model}:correct") or 0),
                incorrect=int(r.get(f"rating:{model}:incorrect") or 0),
                good=int(r.get(f"rating:{model}:good") or 0),
                soso=int(r.get(f"rating:{model}:soso") or 0),
                bad=int(r.get(f"rating:{model}:bad") or 0),
                win=int(r.get(f"rating:{model}:win") or 0),
                lose=int(r.get(f"rating:{model}:lose") or 0),
            )
        )
        if sort_by and hasattr(res[-1], sort_by):
            res.sort(key=lambda x: getattr(x, sort_by), reverse=True)
    return res


@router.get("/objective")
def get_objective_rating_question():
    r = next(get_db())
    keys = r.keys("data:*")
    while True:
        key = random.choice(keys)
        if r.hget(key, "type") == "select":
            break
    models = list(r.smembers("models"))
    model = random.choice(models)
    question = f"选择题：\n{r.hget(key, 'question')}\nA.{r.hget(key, 'A')}\nB.{r.hget(key, 'B')}\nC.{r.hget(key, 'C')}\nD.{r.hget(key, 'D')}\n请你只给出答案序号，不需要解题过程"
    answer = get_llm_response(model, question)
    return [question, model, answer]


@router.get("/subjective", response_model=SubjectiveQuestion)
def get_subjective_rating_question():
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
    

@router.post("/subjective")
def submit_subjective_rating_result(subjective_result: SubjectiveResult):
    r = next(get_db())
    models = r.smembers("models")
    if subjective_result.model_name not in models:
        return {"message": "invalid result"}
    r.incr(f"rating:{subjective_result.model_name}:{subjective_result.evaluation.value}")
    return {"message": "ok"}
    

@router.get("/competitive", response_model=CompetitiveQuestion)
def get_competitive_rating_question():
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


@router.post("/competitive")
def submit_competitive_rating_result(competitive_result: CompetitiveResult):
    r = next(get_db())
    models = r.smembers("models")
    if competitive_result.winner not in models \
        or competitive_result.loser not in models \
        or competitive_result.winner == competitive_result.loser:
        return {"message": "invalid result"}
    r.incr(f"rating:{competitive_result.winner}:win")
    r.incr(f"rating:{competitive_result.loser}:lose")
    return {"message": "ok"}
    