import pytest
from app.engine.normalizer import LosslessNormalizer

def test_lossless_normalizer_firewall():
    normalizer = LosslessNormalizer()
    raw = "SRC=10.10.1.20 DST=172.16.2.10 SP=4521 DP=443 PROTO=TCP ACTION=DENY VENDOR_FLAG=ALERT_1"
    
    event, validation, lineage = normalizer.normalize(raw, source_id="src-fw-1")

    assert event.source.ip == "10.10.1.20"
    assert event.destination.ip == "172.16.2.10"
    assert event.source.port == 4521
    assert event.destination.port == 443
    assert event.network.protocol == "TCP"
    assert event.event.action == "DENY"
    assert event.source_id == "src-fw-1"
    assert event.unmapped["VENDOR_FLAG"] == "ALERT_1"
    assert event.raw_event_reference.raw_id.startswith("raw-")
    assert len(event.raw_event_reference.hash) == 64

    # Check Lineage
    assert len(lineage.mappings) >= 4
    source_ip_mapping = next(m for m in lineage.mappings if m.normalized_field == "source.ip")
    assert source_ip_mapping.raw_field == "SRC"
    assert source_ip_mapping.raw_value == "10.10.1.20"

    # Check Validation
    assert validation.is_valid is True
    assert len(validation.errors) == 0

def test_lossless_normalizer_syslog():
    normalizer = LosslessNormalizer()
    raw = "Aug 26 10:20:15 server01 sshd: Failed password for user admin from 10.10.1.20"
    
    event, validation, lineage = normalizer.normalize(raw, source_id="src-syslog-1")

    assert event.host.name == "server01"
    assert event.user.name == "admin"
    assert event.source.ip == "10.10.1.20"
    assert event.parser.id == "linux-syslog-v1"
    assert validation.is_valid is True
