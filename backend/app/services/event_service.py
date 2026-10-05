import json
import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.db.models import RawLogDB, NormalizedEventDB, FieldLineageDB, ParserRecordDB, SourceRecordDB
from app.core.schema import UniversalEvent, ValidationResult, FieldLineageRecord

class EventService:
    @staticmethod
    async def save_event(
        db: AsyncSession,
        event: UniversalEvent,
        val_result: ValidationResult,
        lineage: FieldLineageRecord,
        raw_payload: str
    ) -> NormalizedEventDB:
        # 1. Store Raw Log
        raw_record = RawLogDB(
            id=event.raw_event_reference.raw_id,
            payload=raw_payload,
            hash=event.raw_event_reference.hash,
            source_id=event.source_id,
            created_at=datetime.datetime.utcnow()
        )
        db.add(raw_record)

        # 2. Store Normalized Event
        event_dict = event.model_dump()
        norm_record = NormalizedEventDB(
            id=event.event.id,
            raw_id=event.raw_event_reference.raw_id,
            source_id=event.source_id,
            parser_id=event.parser.id,
            parser_version=event.parser.version,
            category=event.event.category,
            action=event.event.action,
            outcome=event.event.outcome,
            source_ip=event.source.ip,
            source_port=event.source.port,
            destination_ip=event.destination.ip,
            destination_port=event.destination.port,
            network_protocol=event.network.protocol,
            host_name=event.host.name,
            user_name=event.user.name,
            payload_json=json.dumps(event_dict),
            is_valid=val_result.is_valid,
            created_at=datetime.datetime.utcnow()
        )
        db.add(norm_record)

        # 3. Store Field Lineage
        for item in lineage.mappings:
            lineage_record = FieldLineageDB(
                event_id=event.event.id,
                raw_id=event.raw_event_reference.raw_id,
                normalized_field=item.normalized_field,
                raw_field=item.raw_field,
                raw_value=str(item.raw_value) if item.raw_value is not None else None,
                parser_id=item.parser_id,
                parser_version=item.parser_version
            )
            db.add(lineage_record)

        await db.commit()
        await db.refresh(norm_record)
        return norm_record

    @staticmethod
    async def get_events(
        db: AsyncSession,
        limit: int = 50,
        offset: int = 0,
        source_id: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        stmt = select(NormalizedEventDB, RawLogDB.payload).join(
            RawLogDB, NormalizedEventDB.raw_id == RawLogDB.id
        ).order_by(desc(NormalizedEventDB.created_at)).offset(offset).limit(limit)

        if source_id:
            stmt = stmt.where(NormalizedEventDB.source_id == source_id)
        if category:
            stmt = stmt.where(NormalizedEventDB.category == category)

        result = await db.execute(stmt)
        rows = result.all()

        results = []
        for norm, raw_payload in rows:
            parsed_json = json.loads(norm.payload_json)
            results.append({
                "normalized": parsed_json,
                "raw_payload": raw_payload,
                "db_record": {
                    "id": norm.id,
                    "raw_id": norm.raw_id,
                    "source_id": norm.source_id,
                    "parser_id": norm.parser_id,
                    "is_valid": norm.is_valid,
                    "created_at": (norm.created_at.isoformat() + "Z") if norm.created_at else None
                }
            })
        return results

    @staticmethod
    async def get_lineage(db: AsyncSession, event_id: str) -> Dict[str, Any]:
        stmt = select(FieldLineageDB).where(FieldLineageDB.event_id == event_id)
        res = await db.execute(stmt)
        mappings = res.scalars().all()

        raw_stmt = select(RawLogDB.payload).join(
            NormalizedEventDB, NormalizedEventDB.raw_id == RawLogDB.id
        ).where(NormalizedEventDB.id == event_id)
        raw_res = await db.execute(raw_stmt)
        raw_payload = raw_res.scalar_one_or_none()

        return {
            "event_id": event_id,
            "raw_payload": raw_payload,
            "lineage": [
                {
                    "normalized_field": m.normalized_field,
                    "raw_field": m.raw_field,
                    "raw_value": m.raw_value,
                    "parser_id": m.parser_id,
                    "parser_version": m.parser_version
                }
                for m in mappings
            ]
        }
