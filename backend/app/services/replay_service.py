import asyncio
import logging
from typing import Dict, Any
from app.kafka.producer import producer

logger = logging.getLogger("sarvdrishti.replay")

class ReplayService:
    def __init__(self):
        self.active_replays: Dict[str, Dict[str, Any]] = {}

    async def start_replay(self, replay_id: str, log_content: str, source_id: str = "src-historical") -> Dict[str, Any]:
        lines = [line.strip() for line in log_content.splitlines() if line.strip()]
        total = len(lines)

        self.active_replays[replay_id] = {
            "replay_id": replay_id,
            "source_id": source_id,
            "total_lines": total,
            "processed_lines": 0,
            "status": "processing",
            "progress_percent": 0.0
        }

        # Run background replay
        asyncio.create_task(self._process_replay(replay_id, lines, source_id))
        return self.active_replays[replay_id]

    async def _process_replay(self, replay_id: str, lines: list, source_id: str):
        state = self.active_replays.get(replay_id)
        if not state:
            return

        for idx, line in enumerate(lines, start=1):
            producer.send_raw_event(raw_payload=line, source_id=source_id)
            state["processed_lines"] = idx
            state["progress_percent"] = round((idx / state["total_lines"]) * 100, 2)
            # Small yield to simulate streaming batch throughput
            if idx % 50 == 0:
                await asyncio.sleep(0.01)

        state["status"] = "completed"
        logger.info(f"Historical replay {replay_id} completed: {len(lines)} lines replayed.")

    def get_status(self, replay_id: str) -> Dict[str, Any]:
        return self.active_replays.get(replay_id, {"status": "not_found"})

replay_service = ReplayService()
