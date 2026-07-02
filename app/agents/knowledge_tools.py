from app.database.database import SessionLocal
from app.rag.search import format_search_results, search_knowledge_base


def search_warehouse_documents(query: str) -> str:
    db = SessionLocal()
    try:
        results = search_knowledge_base(db, query)
        return format_search_results(results)
    finally:
        db.close()
