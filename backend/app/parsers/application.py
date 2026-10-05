import re
import json
from typing import Dict, Any, Tuple
from app.parsers.base import BaseParser

class ApplicationParser(BaseParser):
    parser_id = "web-application-v1"
    version = "1.0.0"
    format_name = "application"

    KEY_MAP = {
        "source.ip": ["source_ip", "client_ip", "ip", "src_ip"],
        "user.name": ["user", "username", "account"],
        "network.protocol": ["proto", "scheme"],
        "host.name": ["host", "hostname", "server"],
        "event.created": ["timestamp", "time", "date"]
    }

    def parse(self, raw_payload: str) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
        extracted: Dict[str, Any] = {}
        mappings: Dict[str, str] = {}
        unmapped: Dict[str, Any] = {}

        payload_dict = {}

        # 1. Try parsing JSON first
        trimmed = raw_payload.strip()
        if trimmed.startswith("{") and trimmed.endswith("}"):
            try:
                payload_dict = json.loads(trimmed)
            except Exception:
                payload_dict = {}

        # 2. If not JSON, parse key-value pairs
        if not payload_dict:
            kv_pairs = re.findall(r'([A-Za-z0-9_\.\-]+)=(?:"([^"]*)"|(\S+))', raw_payload)
            for k, val1, val2 in kv_pairs:
                payload_dict[k] = val1 if val1 != "" else val2

        # Extract mapped fields
        for norm_key, candidates in self.KEY_MAP.items():
            for raw_k in candidates:
                if raw_k in payload_dict:
                    extracted[norm_key] = payload_dict.pop(raw_k)
                    mappings[norm_key] = raw_k
                    break

        # Map HTTP specific fields
        method = payload_dict.pop("method", None)
        path = payload_dict.pop("path", None)
        status = payload_dict.pop("status", None)

        if method or path:
            extracted["event.category"] = "web"
            extracted["event.action"] = f"HTTP {method or 'REQUEST'} {path or ''}".strip()
            if method:
                mappings["event.action"] = "method"
            elif path:
                mappings["event.action"] = "path"

        if status is not None:
            try:
                status_code = int(status)
                extracted["event.outcome"] = "success" if status_code < 400 else "failure"
                unmapped["http_status"] = status_code
            except (ValueError, TypeError):
                unmapped["http_status"] = status

        unmapped.update(payload_dict)

        return extracted, mappings, unmapped
