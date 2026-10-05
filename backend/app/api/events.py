from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from app.db.database import get_db
from app.services.event_service import EventService
from app.kafka.producer import producer

router = APIRouter(prefix="/api/events", tags=["Events"])

@router.get("")
async def get_events(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    source_id: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    return await EventService.get_events(db, limit, offset, source_id, category)

@router.get("/lineage/{event_id}")
async def get_event_lineage(
    event_id: str,
    db: AsyncSession = Depends(get_db)
):
    res = await EventService.get_lineage(db, event_id)
    if not res.get("raw_payload"):
        raise HTTPException(status_code=404, detail="Event lineage not found")
    return res

@router.post("/ingest")
async def ingest_single_event(payload: Dict[str, Any]):
    raw_text = payload.get("raw_payload")
    source_id = payload.get("source_id", "api-ingest")
    if not raw_text:
        raise HTTPException(status_code=400, detail="raw_payload is required")
    
    producer.send_raw_event(raw_payload=raw_text, source_id=source_id)
    return {"status": "accepted", "source_id": source_id}
