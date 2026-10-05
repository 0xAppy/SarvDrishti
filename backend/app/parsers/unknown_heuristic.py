import re
from typing import Dict, Any, Tuple
from app.parsers.base import BaseParser

class UnknownHeuristicParser(BaseParser):
    parser_id = "unknown-heuristic-v1"
    version = "1.0.0"
    format_name = "unknown_custom"

    # Regex tokens for pattern recognition
    IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    KV_PATTERN = re.compile(r'([A-Za-z0-9_\-]+)=(?:"([^"]*)"|(\S+))')

    def parse(self, raw_payload: str) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
        extracted: Dict[str, Any] = {}
        mappings: Dict[str, str] = {}
        unmapped: Dict[str, Any] = {}

        # 1. Extract Key-Values
        kv_pairs = self.KV_PATTERN.findall(raw_payload)
        kv_dict = {}
        for k, v1, v2 in kv_pairs:
            kv_dict[k] = v1 if v1 != "" else v2

        # Map inferred keys
        for k, v in list(kv_dict.items()):
            lk = k.lower()
            if lk in ["user", "username", "usr", "account"]:
                extracted["user.name"] = v
                mappings["user.name"] = k
                del kv_dict[k]
            elif lk in ["host", "hostname", "server", "device"]:
                extracted["host.name"] = v
                mappings["host.name"] = k
                del kv_dict[k]
            elif lk in ["ip", "src", "source", "client_ip", "src_ip"]:
                extracted["source.ip"] = v
                mappings["source.ip"] = k
                del kv_dict[k]
            elif lk in ["dst", "dst_ip", "destination", "dest"]:
                extracted["destination.ip"] = v
                mappings["destination.ip"] = k
                del kv_dict[k]
            elif lk in ["action", "op", "operation", "event"]:
                extracted["event.action"] = v
                mappings["event.action"] = k
                del kv_dict[k]

        # 2. If no source IP found yet, search by IP regex
        if "source.ip" not in extracted:
            ips = self.IP_PATTERN.findall(raw_payload)
            if ips:
                extracted["source.ip"] = ips[0]
                mappings["source.ip"] = "inferred_ip"
                if len(ips) > 1:
                    extracted["destination.ip"] = ips[1]
                    mappings["destination.ip"] = "inferred_dst_ip"

        extracted["event.category"] = "custom_unknown"
        extracted["event.outcome"] = "unknown"

        unmapped = kv_dict
        if not unmapped and not extracted:
            unmapped["raw_unstructured"] = raw_payload

        return extracted, mappings, unmapped
