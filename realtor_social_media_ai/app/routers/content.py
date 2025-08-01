from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
import openai
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

router = APIRouter(prefix="/content", tags=["content"])

scheduler = BackgroundScheduler()
scheduler.start()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user():
    return 1


PROMPT_TEMPLATE = """You are a social media assistant for real estate agents.
Generate a {type} post based on the following details:\n{details}\n"""


def generate_ai_content(content_type: str, details: str | None = None) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY", "test")
    prompt = PROMPT_TEMPLATE.format(type=content_type, details=details or "")
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}], max_tokens=200
    )
    return response.choices[0].message.content


def schedule_post_job(post_id: int):
    # Placeholder: push to social API
    print(f"Posting {post_id}")


@router.post("/generate", response_model=schemas.GeneratedContentOut)
def generate_content(
    req: schemas.ContentRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    content = generate_ai_content(req.content_type, req.details)
    record = models.GeneratedContent(
        user_id=user_id, content_type=req.content_type, content=content
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/schedule")
def schedule_post(
    req: schemas.ScheduleRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    if req.scheduled_time > datetime.utcnow().replace(microsecond=0) + timedelta(days=60):
        raise HTTPException(status_code=400, detail="Cannot schedule beyond 60 days")
    post = models.ScheduledPost(
        user_id=user_id,
        platform=req.platform,
        content=req.content,
        scheduled_time=req.scheduled_time,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    scheduler.add_job(
        schedule_post_job,
        'date',
        run_date=req.scheduled_time,
        args=[post.id],
        id=f"post-{post.id}"
    )
    return {"scheduled": post.id}
