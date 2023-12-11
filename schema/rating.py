from enum import Enum

from pydantic import BaseModel, validator

from schema.data import QAData, SelectData


class RatingResult(BaseModel):
    model_name: str
    
    # 客观评测：正确，错误
    correct: int
    incorrect: int
    correct_rate: float = None
    @validator("correct_rate", always=True)
    def get_correct_rate(cls, v, values):
        correct = values.get("correct")
        incorrect = values.get("incorrect")
        return correct / (correct + incorrect) if correct + incorrect else 0
    
    # 主观评测：好，一般，差
    good: int # +1
    soso: int # 0
    bad: int # -1
    subjective_score: float = None
    @validator("subjective_score", always=True)
    def get_subjective_rate(cls, v, values):
        good = values.get("good")
        soso = values.get("soso")
        bad = values.get("bad")
        return (good - bad) / (good + soso + bad) if good + soso + bad else 0
    
    # 对抗评测：胜，负
    win: int
    lose: int
    win_rate: float = None
    @validator("win_rate", always=True)
    def get_win_rate(cls, v, values):
        win = values.get("win")
        lose = values.get("lose")
        return win / (win + lose) if win + lose else 0
    

class ModelAnswer(BaseModel):
    model_name: str
    answer: str


class SubjectiveQuestion(BaseModel):
    question_data: QAData
    answer: ModelAnswer
    
    
class SubjectiveEvaluation(str, Enum):
    good = "good"
    soso = "soso"
    bad = "bad"

    
class SubjectiveResult(BaseModel):
    model_name: str
    evaluation: SubjectiveEvaluation
    
    
class CompetitiveQuestion(BaseModel):
    question_data: QAData
    answer1: ModelAnswer
    answer2: ModelAnswer


class CompetitiveResult(BaseModel):
    winner: str
    loser: str