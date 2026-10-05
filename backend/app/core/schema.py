from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ConfigDict
import uuid
import datetime
import hashlib

class EventMetadata(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    category: str = "unknown"
    action: str = "unknown"
    outcome: str = "unknown"

class SourceEndpoint(BaseModel):
    ip: Optional[str] = None
    port: Optional[int] = None

class DestinationEndpoint(BaseModel):
    ip: Optional[str] = None
    port: Optional[int] = None

class NetworkDetails(BaseModel):
    protocol: Optional[str] = None

class HostDetails(BaseModel):
    name: Optional[str] = None

class UserDetails(BaseModel):
    name: Optional[str] = None

class ParserReference(BaseModel):
    id: str = "unknown-parser"
    version: str = "1.0.0"

class RawEventReference(BaseModel):
    raw_id: str
    hash: str

class UniversalEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    event: EventMetadata = Field(default_factory=EventMetadata)
    source: SourceEndpoint = Field(default_factory=SourceEndpoint)
    destination: DestinationEndpoint = Field(default_factory=DestinationEndpoint)
    network: NetworkDetails = Field(default_factory=NetworkDetails)
    host: HostDetails = Field(default_factory=HostDetails)
    user: UserDetails = Field(default_factory=UserDetails)
    parser: ParserReference = Field(default_factory=ParserReference)
    source_id: str = "src-default"
    raw_event_reference: RawEventReference
    unmapped: Dict[str, Any] = Field(default_factory=dict)

class FieldLineageItem(BaseModel):
    normalized_field: str
    raw_field: str
    raw_value: Any
    parser_id: str
    parser_version: str

class FieldLineageRecord(BaseModel):
    event_id: str
    raw_id: str
    mappings: List[FieldLineageItem]

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
