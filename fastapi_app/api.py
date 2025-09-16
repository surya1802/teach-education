# fastapi_app/api.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Body
from . import schemas
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from .auth import get_current_user  # assume JWT or session auth
# import Django models (available after django.setup() is called in main)
from quiz.models import Subject, Question, Attempt
from pydantic import BaseModel
from .schemas import ( LoginRequest, LoginResponse, SubjectOut, QuestionOut, SubmitRequest, SubmitResponse, AttemptOut )


router = APIRouter()

@router.get("/is-admin")
def is_admin(user=Depends(get_current_user)):
    if not user.is_staff:
        raise HTTPException(status_code=403, detail="Not an admin")
    return {"is_admin": True}

# --- Login endpoint ---
@router.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest):
    user = authenticate(username=payload.username, password=payload.password)
    if user is None:
        # Try email login if username failed
        User = get_user_model()
        try:
            u = User.objects.get(email=payload.username)
            user = authenticate(username=u.username, password=payload.password)
        except User.DoesNotExist:
            user = None

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 👇 This part makes admin redirect work
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff   # 👈 ADD THIS
    }


@router.get("/subjects", response_model=List[schemas.SubjectOut])
def list_subjects():
    qs = Subject.objects.all().order_by("order").values("id", "title", "description", "order")
    return list(qs)

@router.get("/subjects/{subject_id}/questions", response_model=List[schemas.QuestionOut])
def get_questions(subject_id: int):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        raise HTTPException(status_code=404, detail="Subject not found")
    out = []
    for q in subject.questions.all():
        out.append({
            "id": q.id,
            "text": q.text,
            "qtype": q.qtype,
            "difficulty": q.difficulty,
            "choices": q.choices or []
        })
    return out

@router.post("/submit", response_model=schemas.SubmitResponse)
def submit_answers(payload: schemas.SubmitRequest):
    User = get_user_model()
    try:
        user = User.objects.get(username=payload.username)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        subject = Subject.objects.get(pk=payload.subject_id)
    except Subject.DoesNotExist:
        raise HTTPException(status_code=404, detail="Subject not found")

    answers = payload.answers
    qids = [a.question_id for a in answers]
    questions = Question.objects.filter(id__in=qids)
    qmap = {q.id: q for q in questions}

    total = len(answers)
    correct = 0
    details = []

    for a in answers:
        q = qmap.get(a.question_id)
        given = str(a.answer).strip()
        if not q:
            details.append({
                "question_id": a.question_id,
                "given_answer": given,
                "correct_answer": "",
                "correct": False
            })
            continue

        correct_ans = str(q.correct_answer).strip()
        is_correct = False
        if q.qtype == 'mcq':
            is_correct = given == correct_ans
        else:
            is_correct = given.lower() == correct_ans.lower()

        if is_correct:
            correct += 1

        details.append({
            "question_id": q.id,
            "given_answer": given,
            "correct_answer": correct_ans,
            "correct": is_correct
        })

    wrong = total - correct
    percentage = round((correct / total) * 100, 2) if total > 0 else 0.0

    attempt = Attempt.objects.create(
        user=user,
        subject=subject,
        total_questions=total,
        correct=correct,
        wrong=wrong,
        score=percentage,
        details=details,
        finished_at=timezone.now()
    )

    return {
        "total_questions": total,
        "correct": correct,
        "wrong": wrong,
        "percentage": percentage,
        "details": details
    }

# --- Attempts endpoint ---
@router.get("/attempts/{username}", response_model=list[AttemptOut])
def user_attempts(username: str):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    attempts = Attempt.objects.filter(user=user).order_by("-finished_at")
    out = []
    for a in attempts:
        out.append({
            "id": a.id,
            "subject_id": a.subject.id,
            "total_questions": a.total_questions,
            "correct": a.correct,
            "wrong": a.wrong,
            "score": a.score,
            "details": a.details or [],
            "finished_at": a.finished_at.isoformat() if a.finished_at else None
        })
    return out

# Add these endpoints to your api.py file

@router.post("/register")
def register_user(payload: dict):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user = User.objects.create_user(
            username=payload['username'],
            email=payload['email'],
            password=payload['password']
        )
        if 'phone' in payload:
            user.phone = payload['phone']
            user.save()
        
        return {"username": user.username, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Admin endpoints
@router.get("/admin/subjects", response_model=List[schemas.SubjectOut])
def admin_list_subjects():
    qs = Subject.objects.all().order_by("order").values("id", "title", "description", "order")
    return list(qs)

@router.post("/admin/subjects")
def admin_create_subject(payload: dict):
    subject = Subject.objects.create(
        title=payload['title'],
        order=payload.get('order', 0),
        description=payload.get('description', '')
    )
    return {"id": subject.id, "title": subject.title, "order": subject.order}

@router.post("/admin/questions")
def admin_create_question(payload: dict):
    subject = Subject.objects.get(pk=payload['subject_id'])
    question = Question.objects.create(
        subject=subject,
        text=payload['text'],
        qtype=payload['qtype'],
        choices=payload.get('choices'),
        correct_answer=payload['correct_answer'],
        difficulty=payload.get('difficulty', 1)
    )
    return {"id": question.id, "text": question.text}

@router.get("/attempts/history")
def get_attempts_history(username: str):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
        attempts = Attempt.objects.filter(user=user).order_by("-finished_at")
        result = []
        for a in attempts:
            result.append({
                "id": a.id,
                "subject_title": a.subject.title,
                "score": a.score,
                "correct": a.correct,
                "total_questions": a.total_questions,
                "finished_at": a.finished_at.isoformat() if a.finished_at else None
            })
        return result
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    
