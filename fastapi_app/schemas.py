# fastapi_app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    username: str
    is_staff: bool
    email: str = None


class AttemptOut(BaseModel):
    id: int
    subject_id: int
    total_questions: int
    correct: int
    wrong: int
    score: float
    details: list
    finished_at: str | None

class SubjectOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    order: Optional[int] = 0

class QuestionOut(BaseModel):
    id: int
    text: str
    qtype: str
    difficulty: int
    choices: Optional[List[str]] = None

class AnswerIn(BaseModel):
    question_id: int
    answer: str

class SubmitRequest(BaseModel):
    username: str
    subject_id: int
    answers: List[AnswerIn]

class SubmitResultDetail(BaseModel):
    question_id: int
    given_answer: str
    correct_answer: str
    correct: bool

class SubmitResponse(BaseModel):
    total_questions: int
    correct: int
    wrong: int
    percentage: float
    details: List[SubmitResultDetail]

class AttemptOut(BaseModel):
    id: int
    subject_id: int
    total_questions: int
    correct: int
    wrong: int
    score: float
    details: list
    finished_at: Optional[str]