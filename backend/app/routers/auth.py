from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core.security import hash_password
from app.schemas.auth import RegisterRequest, UserResponse
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.deps import get_current_user


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_out = UserResponse(id=user.id, email=user.email, username=user.username)
    data = user_out.model_dump() if hasattr(user_out, "model_dump") else user_out.dict()
    return {"result": data}

@router.post("/login", response_model=dict)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=user.id)

    out = TokenResponse(accessToken=token)
    data = out.model_dump() if hasattr(out, "model_dump") else out.dict()
    return {"result": data}

@router.get("/me", response_model=dict)
def me(current_user: User = Depends(get_current_user)):
    out = UserResponse(id=current_user.id, email=current_user.email, username=current_user.username)
    data = out.model_dump() if hasattr(out, "model_dump") else out.dict()
    return {"result": data}
