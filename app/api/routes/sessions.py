from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.services import conversation_service

router = APIRouter(prefix="/warehouse/sessions", tags=["Sessions"])


class SessionResponse(BaseModel):
    id: int
    user_id: str
    title: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str

    class Config:
        from_attributes = True


@router.post("/", response_model=SessionResponse)
def create_chat_session(
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user),
):
    user_id = user.email if user else "demo-user"
    session = conversation_service.create_session(db, user_id=user_id)
    return session


@router.get("/", response_model=list[SessionResponse])
def list_chat_sessions(
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user),
):
    user_id = user.email if user else "demo-user"
    return conversation_service.list_sessions(db, user_id=user_id)


@router.get("/{session_id}/messages", response_model=list[MessageResponse])
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
):
    session = conversation_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return conversation_service.get_recent_messages(db, session_id, limit=50)
