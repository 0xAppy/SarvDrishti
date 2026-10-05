from typing import Dict, Optional, Type, List, Tuple
from app.parsers.base import BaseParser
from app.parsers.firewall import FirewallParser
from app.parsers.syslog import SyslogParser
from app.parsers.application import ApplicationParser
from app.parsers.unknown_heuristic import UnknownHeuristicParser

class ParserRegistry:
    """
    Registry managing log parsers, versioning, format auto-detection, and registration.
    """

    def __init__(self):
        self._parsers: Dict[str, BaseParser] = {}
        self._format_map: Dict[str, str] = {}  # format_name -> parser_id
        self._register_defaults()

    def _register_defaults(self):
        self.register(FirewallParser())
        self.register(SyslogParser())
        self.register(ApplicationParser())
        self.register(UnknownHeuristicParser())

    def register(self, parser: BaseParser):
        key = f"{parser.parser_id}:{parser.version}"
        self._parsers[key] = parser
        self._parsers[parser.parser_id] = parser  # Also map latest by parser_id
        self._format_map[parser.format_name] = parser.parser_id

    def get_parser(self, parser_id: str, version: Optional[str] = None) -> Optional[BaseParser]:
        if version:
            key = f"{parser_id}:{version}"
            if key in self._parsers:
                return self._parsers[key]
        return self._parsers.get(parser_id)

    def detect_format_and_parser(self, raw_payload: str, hint_source: Optional[str] = None) -> BaseParser:
        payload = raw_payload.strip()

        # 1. Firewall check: Contains key kv patterns like SRC= and DST=
        if ("SRC=" in payload or "src=" in payload) and ("DST=" in payload or "dst=" in payload):
            return self._parsers["firewall-kv-v1"]

        # 2. Application log check: Starts with ISO timestamp or JSON, or method= / status=
        if (payload.startswith("{") and "method" in payload) or "method=" in payload or "status=" in payload:
            return self._parsers["web-application-v1"]

        # 3. Syslog check: Month timestamp + hostname + process
        if any(payload.startswith(m) for m in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
            return self._parsers["linux-syslog-v1"]

        # 4. Fallback to Unknown Heuristic parser
        return self._parsers["unknown-heuristic-v1"]

    def list_parsers(self) -> List[Dict[str, str]]:
        unique = {}
        for key, p in self._parsers.items():
            if ":" in key:  # Format parser_id:version
                unique[key] = {
                    "parser_id": p.parser_id,
                    "version": p.version,
                    "format_name": p.format_name,
                    "status": "active"
                }
        return list(unique.values())

# Global registry singleton
registry = ParserRegistry()
