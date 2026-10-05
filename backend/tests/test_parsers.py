import pytest
from app.parsers.firewall import FirewallParser
from app.parsers.syslog import SyslogParser
from app.parsers.application import ApplicationParser
from app.parsers.unknown_heuristic import UnknownHeuristicParser

def test_firewall_parser():
    parser = FirewallParser()
    raw = "SRC=10.10.1.20 DST=172.16.2.10 SP=4521 DP=443 PROTO=TCP ACTION=DENY VENDOR_TAG=FW_RULE_99"
    extracted, mappings, unmapped = parser.parse(raw)

    assert extracted["source.ip"] == "10.10.1.20"
    assert extracted["destination.ip"] == "172.16.2.10"
    assert extracted["source.port"] == 4521
    assert extracted["destination.port"] == 443
    assert extracted["network.protocol"] == "TCP"
    assert extracted["event.action"] == "DENY"
    assert extracted["event.outcome"] == "failure"
    assert mappings["source.ip"] == "SRC"
    assert unmapped["VENDOR_TAG"] == "FW_RULE_99"

def test_syslog_parser():
    parser = SyslogParser()
    raw = "Aug 26 10:20:15 server01 sshd: Failed password for user admin from 10.10.1.20"
    extracted, mappings, unmapped = parser.parse(raw)

    assert extracted["host.name"] == "server01"
    assert extracted["user.name"] == "admin"
    assert extracted["source.ip"] == "10.10.1.20"
    assert extracted["event.action"] == "login_failed"
    assert extracted["event.outcome"] == "failure"
    assert mappings["source.ip"] == "from_ip"

def test_application_parser():
    parser = ApplicationParser()
    raw = "2026-08-26T10:20:16Z method=POST path=/login user=admin status=401 source_ip=10.10.1.20 response_time_ms=120"
    extracted, mappings, unmapped = parser.parse(raw)

    assert extracted["source.ip"] == "10.10.1.20"
    assert extracted["user.name"] == "admin"
    assert extracted["event.action"] == "HTTP POST /login"
    assert extracted["event.outcome"] == "failure"
    assert unmapped["response_time_ms"] == "120"

def test_unknown_heuristic_parser():
    parser = UnknownHeuristicParser()
    raw = "[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL"
    extracted, mappings, unmapped = parser.parse(raw)

    assert extracted["user.name"] == "john"
    assert extracted["host.name"] == "10.0.0.5"
    assert extracted["event.action"] == "DELETE"
    assert unmapped["file"] == "secret.doc"
