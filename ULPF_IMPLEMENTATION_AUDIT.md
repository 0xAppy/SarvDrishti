# SarvDrishti Implementation Audit

This document contains a strict audit of the SarvDrishti repository based on actual code execution, not documentation or UI mockups.

## 1. Streaming Buffer / Message Queue
*   **Feature**: Asynchronous log ingestion and buffering.
*   **Relevant Files**: `backend/app/kafka/producer.py`, `backend/app/kafka/worker.py`, `docker-compose.yml`.
*   **Actual Execution Path**: `api/events.py` → `producer.send_raw_event()` → `asyncio.Queue` → `worker._process_queue()`.
*   **Dependency**: Python `asyncio.Queue` (Local), Confluent Kafka (Docker).
*   **Real/Simulated/Mock**: Real (Dual-implementation).
*   **Current Status**: **PASS**. The local version uses a robust in-memory `asyncio.Queue` for zero-dependency rapid prototyping. The `docker-compose.yml` provides a real Kafka broker for enterprise scaling. 
*   **Evidence**: Verified via API ingestion; events successfully pass through the worker loop asynchronously.

## 2. Database Persistence
*   **Feature**: Persistent storage of raw payloads and normalized fields.
*   **Relevant Files**: `backend/app/db/database.py`, `backend/app/db/models.py`.
*   **Actual Execution Path**: `worker.py` → `event_service.py` → `SQLAlchemy AsyncSession` → `sarvdrishti.db`.
*   **Dependency**: `aiosqlite` (Local), PostgreSQL (Docker).
*   **Real/Simulated/Mock**: Real.
*   **Current Status**: **PASS**. Fully functional asynchronous database integration. 
*   **Evidence**: Executing `/api/events` successfully retrieves persisted database records.

## 3. Syslog Listener (UDP)
*   **Feature**: Direct UDP port 5140 ingestion.
*   **Relevant Files**: `backend/app/services/syslog_listener.py`.
*   **Actual Execution Path**: `DatagramProtocol` → `datagram_received()` → `producer.send_raw_event(source_id="src-syslog-live")`.
*   **Dependency**: Python `asyncio` networking.
*   **Real/Simulated/Mock**: Real.
*   **Current Status**: **PASS**. A genuine UDP socket server runs as a background task via `main.py`.
*   **Evidence**: Verified via `sudo journalctl -f` ingestion through the UI Testing Sandbox.

## 4. Field Lineage
*   **Feature**: Traceability from normalized fields back to raw payloads.
*   **Relevant Files**: `backend/app/api/events.py`, `backend/app/services/event_service.py`.
*   **Actual Execution Path**: Parsers (`base.py`) return a `mappings_dict` → Stored in `NormalizedEventDB.mapping_metadata` → Retrieved via `/api/events/lineage/{id}`.
*   **Dependency**: None.
*   **Real/Simulated/Mock**: Real.
*   **Current Status**: **PASS**. 
*   **Evidence**: Verified via cURL. The API correctly returned `{"normalized_field":"source.ip", "raw_field":"SRC"}`.

## 5. Lossless Processing (Unmapped Fields)
*   **Feature**: Preservation of unknown vendor fields and raw text.
*   **Relevant Files**: `backend/app/parsers/base.py`, `backend/app/parsers/syslog.py`.
*   **Actual Execution Path**: Parser parses known fields → Places leftover dictionary keys in `unmapped` → Saved to `NormalizedEventDB.unmapped`.
*   **Dependency**: None.
*   **Real/Simulated/Mock**: Real.
*   **Current Status**: **PASS**.
*   **Evidence**: Injected event with `VENDOR_MAGIC=ABC123` correctly surfaced in the `unmapped` JSON column via API check.

## 6. AI Onboarding & Air-Gapped Fallback
*   **Feature**: Generating new parsers for unknown log sources.
*   **Relevant Files**: `backend/app/ai/adapter.py`, `backend/app/services/onboarding_service.py`.
*   **Actual Execution Path**: `/api/onboarding/analyze` → `AIAdapterFactory.get_provider()` → `HeuristicFallbackProvider`.
*   **Dependency**: Standard Python Regex (`re`).
*   **Real/Simulated/Mock**: Real (Fallback heuristic), Simulated (Cloud LLM - currently bypassed/fallback for stability).
*   **Current Status**: **PASS (Air-Gapped)**. The system successfully generates deterministic Regex rules and field mappings entirely offline using a heuristic scanner.
*   **Evidence**: `/api/onboarding/analyze` returned confidence scores and a generated regex without an active internet connection.

## 7. SIEM / Data Lake Integration
*   **Feature**: Consuming normalized events.
*   **Relevant Files**: `backend/app/api/events.py`.
*   **Actual Execution Path**: `GET /api/events` → Returns structured JSON schema.
*   **Dependency**: None.
*   **Real/Simulated/Mock**: Real.
*   **Current Status**: **PASS**. 
*   **Evidence**: API returns exact universal schema required for downstream SIEM ingestion.

## 8. Validation and Dead Letter
*   **Feature**: Validating data types (e.g., valid IPs).
*   **Relevant Files**: `backend/app/core/schema.py`, `backend/app/services/event_service.py`.
*   **Actual Execution Path**: `UniversalEvent(**extracted)` → `ValidationError` caught → `is_valid = False` flag set.
*   **Dependency**: Pydantic.
*   **Real/Simulated/Mock**: Real.
*   **Current Status**: **PARTIAL**. Validation successfully traps errors (verified via invalid IP test) and flags them in the database. However, a dedicated Dead Letter Queue (DLQ) Kafka topic is not explicitly instantiated in the local async implementation.

## 9. Historical Replay
*   **Feature**: Bulk processing of old `.log` files.
*   **Relevant Files**: `backend/app/api/replay.py`, `backend/app/services/replay_service.py`.
*   **Actual Execution Path**: Upload File → Reads lines → Pushes to `producer.send_raw_event()`.
*   **Dependency**: FastAPI UploadFile.
*   **Real/Simulated/Mock**: Real.
*   **Current Status**: **PASS**.

## 10. Performance Benchmarks
*   **Feature**: Events processed per second.
*   **Current Status**: **UI-MOCK / SIMULATED**. The dashboard UI displays `12.5 events/sec` via an arbitrary calculation in `stats.py`. While the system *is* fast (processing local queues instantly), the specific throughput metric on the dashboard is not a real-time moving average calculation. (See SIH_CLAIMS.md).
