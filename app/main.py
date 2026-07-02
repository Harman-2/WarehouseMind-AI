import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

os.environ["GEMINI_API_KEY"] = settings.GOOGLE_API_KEY
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

from app.database.database import engine, Base
from app.models import conversation, documents, events, user, warehouse
from app.api.routes import analytics, auth, documents as documents_routes
from app.api.routes import sessions, warehouse as warehouse_routes
from app.rag.ingest import ensure_upload_dir, ingest_text


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_upload_dir()
    _seed_default_documents()
    yield


def _seed_default_documents():
    from app.database.database import SessionLocal
    from app.models.documents import Document

    db = SessionLocal()
    try:
        if db.query(Document).count() > 0:
            return

        ingest_text(
            db,
            title="Warehouse Safety Manual",
            doc_type="safety",
            filename="safety_manual.txt",
            content="""
            All forklift operators must complete a pre-shift safety inspection.
            Workers must wear high-visibility vests in active loading zones.
            Report spills, blocked aisles, or equipment faults immediately to the shift supervisor.
            Robots below 20 percent battery must be routed to charging before peak order windows.
            """,
        )
        ingest_text(
            db,
            title="Inventory Reorder Policy",
            doc_type="policy",
            filename="inventory_policy.txt",
            content="""
            Reorder any SKU when quantity falls below threshold for two consecutive checks.
            Critical items such as monitors and keyboards require same-day escalation to the inventory manager.
            High-priority orders must not be allocated from stock reserved below threshold.
            Restock requests above 200 units require manager approval.
            """,
        )
        ingest_text(
            db,
            title="Packing Zone SOP",
            doc_type="sop",
            filename="packing_sop.txt",
            content="""
            Maintain at least two active packers in Zone B during peak windows.
            If conveyor downtime exceeds 10 minutes, notify the coordinator and pause new order intake.
            Verify label accuracy before handoff to outbound loading.
            Early departures in packing must trigger immediate shift coverage review.
            """,
        )
    finally:
        db.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(warehouse_routes.router)
app.include_router(analytics.router)
app.include_router(documents_routes.router)
app.include_router(sessions.router)


@app.get("/")
def root():
    return {"message": "WarehouseMind AI running", "version": settings.VERSION}


@app.get("/health")
def health():
    return {"status": "healthy"}
