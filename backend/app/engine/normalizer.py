import hashlib
import uuid
import datetime
from typing import Tuple, Optional, Dict, Any
from app.core.schema import (
    UniversalEvent, EventMetadata, SourceEndpoint, DestinationEndpoint,
    NetworkDetails, HostDetails, UserDetails, ParserReference,
    RawEventReference, FieldLineageRecord, FieldLineageItem, ValidationResult
)
from app.core.validator import EventValidator
from app.parsers.registry import registry

class LosslessNormalizer:
    """
    Core Normalization Engine.
    Transforms raw log strings into Universal Event Schema representations while
    maintaining 100% information preservation and generating field lineage links.
    """

    def __init__(self):
        self.validator = EventValidator()

    def normalize(
        self,
        raw_payload: str,
        source_id: str = "src-default",
        parser_id_override: Optional[str] = None
    ) -> Tuple[UniversalEvent, ValidationResult, FieldLineageRecord]:
        
        raw_bytes = raw_payload.encode("utf-8")
        raw_hash = hashlib.sha256(raw_bytes).hexdigest()
        raw_id = f"raw-{uuid.uuid4()}"

        raw_ref = RawEventReference(raw_id=raw_id, hash=raw_hash)

        # 1. Select parser
        if parser_id_override:
            parser = registry.get_parser(parser_id_override) or registry.detect_format_and_parser(raw_payload)
        else:
            parser = registry.detect_format_and_parser(raw_payload)

        # 2. Extract fields
        extracted, raw_field_map, unmapped = parser.parse(raw_payload)

        # 3. Populate Universal Event components
        event_meta = EventMetadata(
            created=extracted.get("event.created", datetime.datetime.now(datetime.timezone.utc).isoformat()),
            category=extracted.get("event.category", "system"),
            action=extracted.get("event.action", "unknown"),
            outcome=extracted.get("event.outcome", "unknown")
        )

        source_ep = SourceEndpoint(
            ip=extracted.get("source.ip"),
            port=extracted.get("source.port")
        )

        dest_ep = DestinationEndpoint(
            ip=extracted.get("destination.ip"),
            port=extracted.get("destination.port")
        )

        net_details = NetworkDetails(
            protocol=extracted.get("network.protocol")
        )

        host_details = HostDetails(
            name=extracted.get("host.name")
        )

        user_details = UserDetails(
            name=extracted.get("user.name")
        )

        parser_ref = ParserReference(
            id=parser.parser_id,
            version=parser.version
        )

        universal_event = UniversalEvent(
            event=event_meta,
            source=source_ep,
            destination=dest_ep,
            network=net_details,
            host=host_details,
            user=user_details,
            parser=parser_ref,
            source_id=source_id,
            raw_event_reference=raw_ref,
            unmapped=unmapped
        )

        # 4. Generate Lineage items
        lineage_items = []
        for norm_k, raw_k in raw_field_map.items():
            val = extracted.get(norm_k)
            lineage_items.append(FieldLineageItem(
                normalized_field=norm_k,
                raw_field=raw_k,
                raw_value=val,
                parser_id=parser.parser_id,
                parser_version=parser.version
            ))

        lineage_record = FieldLineageRecord(
            event_id=universal_event.event.id,
            raw_id=raw_id,
            mappings=lineage_items
        )

        # 5. Validation
        val_result = self.validator.validate(universal_event)

        return universal_event, val_result, lineage_record
