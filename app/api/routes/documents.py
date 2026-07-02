import os
import shutil

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database.database import get_db
from app.models.documents import Document
from app.models.user import User
from app.rag.ingest import ensure_upload_dir, ingest_pdf, ingest_text
from app.rag.search import search_knowledge_base

router = APIRouter(prefix="/warehouse/documents", tags=["RAG Documents"])


class TextDocumentRequest(BaseModel):
    title: str
    content: str
    doc_type: str = "policy"


class SearchRequest(BaseModel):
    query: str
    limit: int = 4


@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin", "manager", "viewer")),
):
    documents = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    return [
        {
            "id": doc.id,
            "title": doc.title,
            "filename": doc.filename,
            "doc_type": doc.doc_type,
            "uploaded_at": doc.uploaded_at,
            "chunk_count": len(doc.chunks),
        }
        for doc in documents
    ]


@router.post("/upload")
async def upload_document(
    title: str = Form(...),
    doc_type: str = Form("policy"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin", "manager")),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported")

    upload_dir = ensure_upload_dir()
    destination = os.path.join(upload_dir, file.filename)

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = ingest_pdf(db, destination, title=title, doc_type=doc_type)
    return {
        "id": document.id,
        "title": document.title,
        "filename": document.filename,
        "doc_type": document.doc_type,
        "chunk_count": len(document.chunks),
    }


@router.post("/text")
def create_text_document(
    payload: TextDocumentRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin", "manager")),
):
    document = ingest_text(
        db,
        title=payload.title,
        content=payload.content,
        doc_type=payload.doc_type,
    )
    return {
        "id": document.id,
        "title": document.title,
        "doc_type": document.doc_type,
        "chunk_count": len(document.chunks),
    }


@router.post("/search")
def search_documents(
    payload: SearchRequest,
    db: Session = Depends(get_db),
):
    return search_knowledge_base(db, payload.query, limit=payload.limit)
