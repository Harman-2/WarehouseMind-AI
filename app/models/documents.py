from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    doc_type = Column(String, default="policy")
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    chunk_index = Column(Integer, default=0)
    content = Column(Text, nullable=False)

    document = relationship("Document", back_populates="chunks")
