from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_current_user,
    hash_password,
    require_role,
    verify_password,
)
from app.database.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "viewer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.role not in {"admin", "manager", "viewer"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    user_count = db.query(User).count()
    if user_count > 0 and payload.role == "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin accounts can only be created by an existing admin",
        )

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = "admin" if user_count == 0 else payload.role

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.email, user.role)
    return TokenResponse(
        access_token=token,
        role=user.role,
        full_name=user.full_name,
    )


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(require_role("admin", "manager", "viewer"))):
    return user
