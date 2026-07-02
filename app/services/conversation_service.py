from sqlalchemy.orm import Session

from app.models.conversation import ChatMessage, ChatSession


def create_session(db: Session, user_id: str, title: str = "Warehouse Chat") -> ChatSession:
    session = ChatSession(user_id=user_id, title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int) -> ChatSession | None:
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()


def list_sessions(db: Session, user_id: str, limit: int = 20) -> list[ChatSession]:
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
        .limit(limit)
        .all()
    )


def add_message(
    db: Session,
    session_id: int,
    role: str,
    content: str,
) -> ChatMessage:
    message = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(message)

    session = get_session(db, session_id)
    if session:
        session.title = content[:60] + ("..." if len(content) > 60 else "")

    db.commit()
    db.refresh(message)
    return message


def get_recent_messages(
    db: Session,
    session_id: int,
    limit: int = 10,
) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()[::-1]
    )


def format_history(messages: list[ChatMessage]) -> str:
    if not messages:
        return ""

    lines = ["Previous conversation:"]
    for message in messages:
        speaker = "User" if message.role == "user" else "Assistant"
        lines.append(f"{speaker}: {message.content}")
    return "\n".join(lines)
