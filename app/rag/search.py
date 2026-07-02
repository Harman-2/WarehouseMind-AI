import re

from sqlalchemy.orm import Session

from app.models.documents import Document, DocumentChunk


def _score_chunk(query: str, content: str) -> float:
    query_terms = {term for term in re.findall(r"[a-z0-9]+", query.lower()) if len(term) > 2}
    if not query_terms:
        return 0.0

    content_lower = content.lower()
    hits = sum(1 for term in query_terms if term in content_lower)
    return hits / len(query_terms)


def search_knowledge_base(db: Session, query: str, limit: int = 4) -> list[dict]:
    chunks = db.query(DocumentChunk, Document).join(Document).all()
    ranked = []

    for chunk, document in chunks:
        score = _score_chunk(query, chunk.content)
        if score <= 0:
            continue
        ranked.append(
            {
                "score": score,
                "title": document.title,
                "doc_type": document.doc_type,
                "content": chunk.content,
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:limit]


def format_search_results(results: list[dict]) -> str:
    if not results:
        return "No relevant warehouse documents found."

    sections = []
    for item in results:
        sections.append(
            f"[{item['doc_type'].upper()}] {item['title']}\n{item['content']}"
        )
    return "\n\n".join(sections)
