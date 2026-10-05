import datetime
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey, JSON
from app.db.database import Base

class RawLogDB(Base):
    __tablename__ = "raw_logs"

    id = Column(String, primary_key=True, index=True)
    payload = Column(Text, nullable=False)
    hash = Column(String(64), nullable=False, index=True)
    source_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class NormalizedEventDB(Base):
    __tablename__ = "normalized_events"

    id = Column(String, primary_key=True, index=True)
    raw_id = Column(String, ForeignKey("raw_logs.id"), nullable=False, index=True)
    source_id = Column(String, nullable=False, index=True)
    parser_id = Column(String, nullable=False)
    parser_version = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    outcome = Column(String, nullable=False)
    source_ip = Column(String, nullable=True, index=True)
    source_port = Column(Integer, nullable=True)
    destination_ip = Column(String, nullable=True, index=True)
    destination_port = Column(Integer, nullable=True)
    network_protocol = Column(String, nullable=True)
    host_name = Column(String, nullable=True, index=True)
    user_name = Column(String, nullable=True, index=True)
    payload_json = Column(Text, nullable=False)
    is_valid = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class FieldLineageDB(Base):
    __tablename__ = "field_lineage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String, ForeignKey("normalized_events.id"), nullable=False, index=True)
    raw_id = Column(String, ForeignKey("raw_logs.id"), nullable=False, index=True)
    normalized_field = Column(String, nullable=False)
    raw_field = Column(String, nullable=False)
    raw_value = Column(Text, nullable=True)
    parser_id = Column(String, nullable=False)
    parser_version = Column(String, nullable=False)

class ParserRecordDB(Base):
    __tablename__ = "parsers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    format = Column(String, nullable=False)
    version = Column(String, nullable=False)
    status = Column(String, default="active", index=True)
    config_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SourceRecordDB(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    ingestion_method = Column(String, nullable=False)
    parser_id = Column(String, nullable=False)
    status = Column(String, default="active", index=True)
    last_event_at = Column(DateTime, nullable=True)

class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
