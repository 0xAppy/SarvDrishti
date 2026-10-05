import json
import uuid
import datetime
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.adapter import AIAdapterFactory
from app.parsers.base import BaseParser
from app.parsers.registry import registry
from app.db.models import ParserRecordDB, AuditLogDB
from app.core.schema import UniversalEvent, ValidationResult

class GeneratedDynamicParser(BaseParser):
    def __init__(self, parser_id: str, version: str, mappings: List[Dict[str, Any]], regex_pattern: str):
        self.parser_id = parser_id
        self.version = version
        self.format_name = "custom_ai_generated"
        self.mappings = mappings
        self.regex_pattern = regex_pattern

    def parse(self, raw_payload: str):
        extracted: Dict[str, Any] = {}
        mappings_dict: Dict[str, str] = {}
        unmapped: Dict[str, Any] = {}

        import re
        kv_pairs = re.findall(r'([A-Za-z0-9_\-\.]+)=(?:"([^"]*)"|(\S+))', raw_payload)
        kv_dict = {k: (v1 if v1 != "" else v2) for k, v1, v2 in kv_pairs}

        for item in self.mappings:
            raw_k = item.get("raw_key")
            target_field = item.get("target_schema_field")
            if raw_k in kv_dict:
                val = kv_dict.pop(raw_k)
                extracted[target_field] = val
                mappings_dict[target_field] = raw_k

        extracted["event.category"] = "custom_onboarded"
        extracted["event.action"] = "custom_event"

        unmapped = kv_dict
        return extracted, mappings_dict, unmapped

class OnboardingService:
    @staticmethod
    async def analyze_sample(sample_log: str) -> Dict[str, Any]:
        provider = AIAdapterFactory.get_provider()
        analysis = await provider.analyze_sample_log(sample_log)
        
        proposed_parser_id = f"custom-parser-{uuid.uuid4().hex[:6]}"
        analysis["proposed_parser_id"] = proposed_parser_id
        analysis["version"] = "1.0.0"
        return analysis

    @staticmethod
    async def validate_proposed_parser(
        sample_log: str,
        parser_id: str,
        version: str,
        mappings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        
        dynamic_parser = GeneratedDynamicParser(
            parser_id=parser_id,
            version=version,
            mappings=mappings,
            regex_pattern=""
        )

        extracted, mappings_dict, unmapped = dynamic_parser.parse(sample_log)

        # Basic check
        pass_validation = len(extracted) > 0 or len(unmapped) > 0
        return {
            "parser_id": parser_id,
            "version": version,
            "validation_status": "PASS" if pass_validation else "FAIL",
            "extracted_fields": extracted,
            "field_mappings": mappings_dict,
            "unmapped_fields": unmapped,
            "test_sample": sample_log
        }

    @staticmethod
    async def approve_parser(
        db: AsyncSession,
        parser_id: str,
        version: str,
        format_name: str,
        mappings: List[Dict[str, Any]],
        regex_pattern: str
    ) -> ParserRecordDB:
        
        dynamic_parser = GeneratedDynamicParser(
            parser_id=parser_id,
            version=version,
            mappings=mappings,
            regex_pattern=regex_pattern
        )
        registry.register(dynamic_parser)

        record = ParserRecordDB(
            id=f"{parser_id}:{version}",
            name=f"Parser {parser_id}",
            format=format_name,
            version=version,
            status="active",
            config_json=json.dumps({"mappings": mappings, "regex": regex_pattern}),
            created_at=datetime.datetime.utcnow()
        )
        db.add(record)

        audit = AuditLogDB(
            action="parser_approved",
            details=f"Approved AI-generated parser {parser_id}:{version}",
            timestamp=datetime.datetime.utcnow()
        )
        db.add(audit)

        await db.commit()
        await db.refresh(record)
        return record
