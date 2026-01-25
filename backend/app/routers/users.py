from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db import models
from app.schemas.auth import UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    result = []
    for u in users:
        ur = UserResponse(id=u.id, email=u.email, username=u.username, is_admin=False)
        result.append(ur)
    return result

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    ur = UserResponse(id=user.id, email=user.email, username=user.username, is_admin=False)
    return ur

@router.put("/{user_id}/makeAdmin")
def make_admin(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Nëse do kishim kolumnën isAdmin në DB: user.is_admin = True
    db.commit()
    return {"message": "User is now admin (simulated)"}

@router.post("", response_model=dict)
def create_user(payload: UserResponse, db: Session = Depends(get_db)):
    # Syncing user from frontend (Firebase) to local SQL database
    user = db.query(models.User).filter(models.User.id == payload.id).first()
    if not user:
        user = models.User(
            id=payload.id,
            email=payload.email,
            username=payload.username or payload.email.split("@")[0],
            password_hash="FIREBASE_USER", # Mark as firebase user
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return {
        "result": UserResponse(id=user.id, email=user.email, username=user.username, is_admin=False).model_dump(by_alias=True),
        "errors": [],
        "messages": ["User synced"]
    }
