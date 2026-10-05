import asyncio
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.engine.normalizer import LosslessNormalizer
from app.services.event_service import EventService
from app.db.database import AsyncSessionLocal
from app.kafka.producer import in_memory_queue

logger = logging.getLogger("sarvdrishti.worker")

class PipelineWorker:
    """
    Log processing pipeline worker.
    Consumes raw event messages, executes normalizer, validates schema,
    persists events/lineage into database, and handles dead-letter logs.
    """

    def __init__(self):
        self.normalizer = LosslessNormalizer()
        self.is_running = False
        self.processed_count = 0
        self.failed_count = 0

    async def process_message(self, db: AsyncSession, raw_payload: str, source_id: str):
        try:
            event, val_result, lineage = self.normalizer.normalize(
                raw_payload=raw_payload,
                source_id=source_id
            )
            await EventService.save_event(
                db=db,
                event=event,
                val_result=val_result,
                lineage=lineage,
                raw_payload=raw_payload
            )
            self.processed_count += 1
            if not val_result.is_valid:
                self.failed_count += 1
        except Exception as e:
            logger.error(f"Error processing payload in worker: {e}")
            self.failed_count += 1

    async def start_worker_loop(self):
        self.is_running = True
        logger.info("SarvDrishti Worker processing loop started.")
        while self.is_running:
            if in_memory_queue:
                msg = in_memory_queue.pop(0)
                async with AsyncSessionLocal() as db:
                    await self.process_message(
                        db=db,
                        raw_payload=msg["raw_payload"],
                        source_id=msg.get("source_id", "src-default")
                    )
            else:
                await asyncio.sleep(0.1)

worker = PipelineWorker()
