from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import SessionLocal
from app.db.models import QueryLog

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/{tenant_id}")
def get_metrics(
    tenant_id: str,
):
    db: Session = SessionLocal()

    total_queries = db.query(QueryLog).filter(
        QueryLog.tenant_id == tenant_id
    ).count()

    avg_duration = db.query(func.avg(QueryLog.duration_ms)).filter(
        QueryLog.tenant_id == tenant_id
    ).scalar()

    db.close()

    return {
        "tenant_id": tenant_id,
        "total_queries": total_queries,
        "average_duration_ms": int(avg_duration) if avg_duration else 0
    }