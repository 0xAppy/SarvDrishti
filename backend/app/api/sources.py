from fastapi import APIRouter
from typing import List, Dict, Any
import datetime

router = APIRouter(prefix="/api/sources", tags=["Sources"])

DEFAULT_SOURCES = [
    {
        "id": "src-firewall-01",
        "name": "Enterprise Perimeter Firewall",
        "type": "firewall",
        "ingestion_method": "API / Log Stream",
        "parser_assigned": "firewall-kv-v1",
        "status": "active",
        "last_received_event": datetime.datetime.utcnow().isoformat()
    },
    {
        "id": "src-syslog-live",
        "name": "Linux Core Syslog (UDP 5140)",
        "type": "syslog",
        "ingestion_method": "Syslog UDP Listener",
        "parser_assigned": "linux-syslog-v1",
        "status": "active",
        "last_received_event": datetime.datetime.utcnow().isoformat()
    },
    {
        "id": "src-webapp-01",
        "name": "Web & Auth Server Logs",
        "type": "application",
        "ingestion_method": "File Upload / REST API",
        "parser_assigned": "web-application-v1",
        "status": "active",
        "last_received_event": datetime.datetime.utcnow().isoformat()
    },
    {
        "id": "src-unknown-01",
        "name": "Custom Proprietary Security Log",
        "type": "unknown",
        "ingestion_method": "AI Onboarding Studio",
        "parser_assigned": "unknown-heuristic-v1",
        "status": "pending_onboarding",
        "last_received_event": datetime.datetime.utcnow().isoformat()
    }
]

@router.get("")
async def list_sources() -> List[Dict[str, Any]]:
    return DEFAULT_SOURCES
