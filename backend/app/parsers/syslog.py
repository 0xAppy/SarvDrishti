import re
from typing import Dict, Any, Tuple
from datetime import datetime
from app.parsers.base import BaseParser

class SyslogParser(BaseParser):
    parser_id = "linux-syslog-v1"
    version = "1.0.0"
    format_name = "syslog"

    # Regex patterns for RFC3164 Syslog & SSHD authentication logs
    SYSLOG_HEADER_PATTERN = re.compile(
        r'^(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<process>[^:]+):\s+(?P<message>.*)$'
    )

    FAILED_PWD_PATTERN = re.compile(
        r'Failed password for (?:invalid user |user )?(?P<user>\S+) from (?P<source_ip>\S+)(?: port (?P<source_port>\d+))?'
    )

    ACCEPTED_PWD_PATTERN = re.compile(
        r'Accepted password for (?:user )?(?P<user>\S+) from (?P<source_ip>\S+)(?: port (?P<source_port>\d+))?'
    )

    def parse(self, raw_payload: str) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
        extracted: Dict[str, Any] = {}
        mappings: Dict[str, str] = {}
        unmapped: Dict[str, Any] = {}

        match = self.SYSLOG_HEADER_PATTERN.match(raw_payload.strip())
        if match:
            groups = match.groupdict()
            timestamp_raw = groups.get("timestamp")
            host_raw = groups.get("host")
            process_raw = groups.get("process")
            message_raw = groups.get("message")

            if host_raw:
                extracted["host.name"] = host_raw
                mappings["host.name"] = "host"

            if process_raw:
                unmapped["process"] = process_raw

            extracted["event.category"] = "authentication"

            # Parse message content
            if message_raw:
                fail_match = self.FAILED_PWD_PATTERN.search(message_raw)
                acc_match = self.ACCEPTED_PWD_PATTERN.search(message_raw)

                if fail_match:
                    p = fail_match.groupdict()
                    extracted["event.action"] = "login_failed"
                    extracted["event.outcome"] = "failure"
                    if p.get("user"):
                        extracted["user.name"] = p["user"]
                        mappings["user.name"] = "user"
                    if p.get("source_ip"):
                        extracted["source.ip"] = p["source_ip"]
                        mappings["source.ip"] = "from_ip"
                    if p.get("source_port"):
                        try:
                            extracted["source.port"] = int(p["source_port"])
                            mappings["source.port"] = "port"
                        except ValueError:
                            pass
                elif acc_match:
                    p = acc_match.groupdict()
                    extracted["event.action"] = "login_success"
                    extracted["event.outcome"] = "success"
                    if p.get("user"):
                        extracted["user.name"] = p["user"]
                        mappings["user.name"] = "user"
                    if p.get("source_ip"):
                        extracted["source.ip"] = p["source_ip"]
                        mappings["source.ip"] = "from_ip"
                    if p.get("source_port"):
                        try:
                            extracted["source.port"] = int(p["source_port"])
                            mappings["source.port"] = "port"
                        except ValueError:
                            pass
                else:
                    unmapped["syslog_message"] = message_raw
        else:
            unmapped["unparsed_raw"] = raw_payload

        return extracted, mappings, unmapped
