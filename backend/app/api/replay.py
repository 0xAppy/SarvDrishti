import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.replay_service import replay_service

router = APIRouter(prefix="/api/replay", tags=["Replay"])

@router.post("/upload")
async def upload_historical_log(
    file: UploadFile = File(...),
    source_id: str = Form("src-historical")
):
    content_bytes = await file.read()
    content_str = content_bytes.decode("utf-8", errors="replace")
    if not content_str.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    replay_id = f"replay-{uuid.uuid4().hex[:8]}"
    state = await replay_service.start_replay(
        replay_id=replay_id,
        log_content=content_str,
        source_id=source_id
    )
    return state

@router.get("/status/{replay_id}")
async def get_replay_status(replay_id: str):
    return replay_service.get_status(replay_id)
