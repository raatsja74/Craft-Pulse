from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/profile", tags=["profile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Placeholder for getting current user

def get_current_user():
    # In a real app you'd validate JWT here
    return 1  # user id placeholder


@router.post("/setup", response_model=schemas.ProfileSetup)
def setup_profile(data: schemas.ProfileSetup, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    profile = models.UserProfile(user_id=user_id, **data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return data
