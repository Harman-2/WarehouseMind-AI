import os
import re
from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.documents import Document, DocumentChunk

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def _split_text(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start = end - CHUNK_OVERLAP
    return chunks


def ingest_pdf(
    db: Session,
    file_path: str,
    title: str,
    doc_type: str = "policy",
) -> Document:
    reader = PdfReader(file_path)
    pages = [page.extract_text() or "" for page in reader.pages]
    full_text = "\n".join(pages)

    document = Document(
        title=title,
        filename=Path(file_path).name,
        doc_type=doc_type,
    )
    db.add(document)
    db.flush()

    for index, chunk in enumerate(_split_text(full_text)):
        db.add(
            DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
            )
        )

    db.commit()
    db.refresh(document)
    return document


def ingest_text(
    db: Session,
    title: str,
    content: str,
    doc_type: str = "policy",
    filename: str = "manual.txt",
) -> Document:
    document = Document(title=title, filename=filename, doc_type=doc_type)
    db.add(document)
    db.flush()

    for index, chunk in enumerate(_split_text(content)):
        db.add(
            DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
            )
        )

    db.commit()
    db.refresh(document)
    return document


def ensure_upload_dir() -> str:
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir
