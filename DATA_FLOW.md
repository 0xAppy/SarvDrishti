# SarvDrishti Data Flow Specification

## Core Data Flow Sequence

1. **Ingestion**:
   - Log sources (Firewall, Syslog, Web Server, File Upload) send raw log text payloads into SarvDrishti.

2. **Buffering**:
   - The REST API / Syslog listener generates a JSON message `{"raw_payload": "...", "source_id": "..."}` and pushes it into Kafka topic `raw-events`.

3. **Processing Worker**:
   - Pipeline worker consumes the payload.
   - Calculates SHA-256 payload hash and generates `raw_id`.

4. **Format Auto-Detection & Parsing**:
   - `ParserRegistry` analyzes format signatures.
   - Executes selected `BaseParser` instance returning `(extracted_fields, raw_field_map, unmapped_fields)`.

5. **Universal Normalization**:
   - Constructs Pydantic `UniversalEvent` model.
   - Stores extra unmapped fields in `unmapped` dictionary.

6. **Validation Engine**:
   - Validates required fields, IP formats, port bounds [1-65535], and ISO timestamps.

7. **Dual-Store Persistence**:
   - Writes `RawLogDB` record (lossless raw payload).
   - Writes `NormalizedEventDB` record (Universal Schema).
   - Writes `FieldLineageDB` records (field-level mappings).

8. **Dashboard Visualization**:
   - Events are rendered in the Event Explorer.
   - Clicking a field loads provenance details in the Lineage Viewer.
