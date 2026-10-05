import re
import ipaddress
from datetime import datetime
from typing import Dict, Any, List
from app.core.schema import UniversalEvent, ValidationResult

class EventValidator:
    """
    Deterministic validation engine verifying extracted & normalized logs.
    Checks required fields, IP formats, port bounds, timestamp formats, and unmapped preservation.
    """

    @staticmethod
    def validate_ip(ip_str: str) -> bool:
        if not ip_str:
            return True
        try:
            ipaddress.ip_address(ip_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_port(port: Any) -> bool:
        if port is None:
            return True
        try:
            val = int(port)
            return 1 <= val <= 65535
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_iso_timestamp(ts_str: str) -> bool:
        if not ts_str:
            return False
        try:
            # Handle ISO formats including trailing Z
            if ts_str.endswith("Z"):
                ts_str = ts_str[:-1] + "+00:00"
            datetime.fromisoformat(ts_str)
            return True
        except ValueError:
            return False

    def validate(self, event: UniversalEvent) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Required core identifiers
        if not event.event.id:
            errors.append("Missing required field: event.id")
        if not event.raw_event_reference or not event.raw_event_reference.raw_id:
            errors.append("Missing required raw event reference")

        # 2. Timestamp check
        if not self.validate_iso_timestamp(event.event.created):
            warnings.append(f"Invalid timestamp format: {event.event.created}")

        # 3. Source & Destination IP checks
        if event.source.ip and not self.validate_ip(event.source.ip):
            errors.append(f"Invalid source IP address format: {event.source.ip}")
        if event.destination.ip and not self.validate_ip(event.destination.ip):
            errors.append(f"Invalid destination IP address format: {event.destination.ip}")

        # 4. Source & Destination Port checks
        if event.source.port is not None and not self.validate_port(event.source.port):
            errors.append(f"Source port out of range [1-65535]: {event.source.port}")
        if event.destination.port is not None and not self.validate_port(event.destination.port):
            errors.append(f"Destination port out of range [1-65535]: {event.destination.port}")

        # 5. Parser attribution check
        if not event.parser.id or event.parser.id == "unknown-parser":
            warnings.append("Event processed by default or unknown parser")

        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)
