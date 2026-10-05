from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.onboarding_service import OnboardingService

router = APIRouter(prefix="/api/onboarding", tags=["AI Onboarding"])

class AnalyzeRequest(BaseModel):
    sample_log: str

class ValidateRequest(BaseModel):
    sample_log: str
    parser_id: str
    version: str = "1.0.0"
    mappings: List[Dict[str, Any]]

class ApproveRequest(BaseModel):
    parser_id: str
    version: str = "1.0.0"
    format_name: str = "custom_onboarded"
    mappings: List[Dict[str, Any]]
    regex_pattern: Optional[str] = ""

@router.post("/analyze")
async def analyze_log(req: AnalyzeRequest):
    if not req.sample_log.strip():
        raise HTTPException(status_code=400, detail="sample_log cannot be empty")
    return await OnboardingService.analyze_sample(req.sample_log)

@router.post("/validate")
async def validate_parser(req: ValidateRequest):
    return await OnboardingService.validate_proposed_parser(
        sample_log=req.sample_log,
        parser_id=req.parser_id,
        version=req.version,
        mappings=req.mappings
    )

@router.post("/approve")
async def approve_parser(req: ApproveRequest, db: AsyncSession = Depends(get_db)):
    record = await OnboardingService.approve_parser(
        db=db,
        parser_id=req.parser_id,
        version=req.version,
        format_name=req.format_name,
        mappings=req.mappings,
        regex_pattern=req.regex_pattern or ""
    )
    return {"status": "approved", "parser_id": record.id, "version": record.version}
