from fastapi import APIRouter
from app.parsers.registry import registry
from typing import List, Dict, Any

router = APIRouter(prefix="/api/parsers", tags=["Parsers"])

@router.get("")
async def list_parsers() -> List[Dict[str, Any]]:
    return registry.list_parsers()
