import re
from typing import Dict, Any, Tuple
from app.parsers.base import BaseParser

class FirewallParser(BaseParser):
    parser_id = "firewall-kv-v1"
    version = "1.0.0"
    format_name = "firewall_kv"

    # Known field mappings: normalized key -> raw key candidates
    KEY_MAP = {
        "source.ip": ["SRC", "src", "src_ip", "source_ip"],
        "destination.ip": ["DST", "dst", "dst_ip", "destination_ip"],
        "source.port": ["SP", "sp", "src_port", "source_port"],
        "destination.port": ["DP", "dp", "dst_port", "destination_port"],
        "network.protocol": ["PROTO", "proto", "protocol"],
        "event.action": ["ACTION", "action", "act"],
        "host.name": ["HOST", "host", "hostname", "fw_name"]
    }

    def parse(self, raw_payload: str) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
        extracted: Dict[str, Any] = {}
        mappings: Dict[str, str] = {}
        unmapped: Dict[str, Any] = {}

        # Key-Value extraction: KEY=VALUE or KEY="VALUE"
        kv_pairs = re.findall(r'([A-Za-z0-9_\.\-]+)=(?:"([^"]*)"|(\S+))', raw_payload)
        found_keys = {}
        for key, val1, val2 in kv_pairs:
            value = val1 if val1 != "" else val2
            found_keys[key] = value

        # Map known fields
        for norm_key, candidates in self.KEY_MAP.items():
            for raw_k in candidates:
                if raw_k in found_keys:
                    val = found_keys.pop(raw_k)
                    # Convert ports to int if applicable
                    if norm_key in ["source.port", "destination.port"]:
                        try:
                            val = int(val)
                        except (ValueError, TypeError):
                            pass
                    extracted[norm_key] = val
                    mappings[norm_key] = raw_k
                    break

        # Set default categories
        extracted["event.category"] = "network"
        if "event.action" in extracted:
            act = str(extracted["event.action"]).lower()
            extracted["event.outcome"] = "success" if act in ["allow", "accept", "permit"] else "failure"

        # Any remaining key-values go to unmapped for 100% information preservation
        unmapped = found_keys

        return extracted, mappings, unmapped
