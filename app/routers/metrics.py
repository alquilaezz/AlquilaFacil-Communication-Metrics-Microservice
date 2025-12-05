from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from .. import models, schemas
from ..deps import get_db, get_current_user, CurrentUser

router = APIRouter(prefix="/api/v1/metrics", tags=["Metrics"])

# --- POST /api/v1/metrics ---

@router.post("", response_model=schemas.MetricOut)
def create_metric(
    payload: schemas.MetricCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    metric = models.Metric(
        event_name=payload.event_name,
        user_id=current_user.id,
        session_id=payload.session_id,
        timestamp=payload.timestamp or datetime.utcnow(),
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

# ---- OPCIONAL: GET por usuario ----

@router.get("/user/{user_id}", response_model=List[schemas.MetricOut])
def get_metrics_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    metrics = (
        db.query(models.Metric)
        .filter(models.Metric.user_id == user_id)
        .order_by(models.Metric.timestamp.desc())
        .all()
    )
    return metrics

# ---- OPCIONAL: GET por sesión ----

@router.get("/session/{session_id}", response_model=List[schemas.MetricOut])
def get_metrics_by_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    metrics = (
        db.query(models.Metric)
        .filter(models.Metric.session_id == session_id)
        .order_by(models.Metric.timestamp.desc())
        .all()
    )
    return metrics
