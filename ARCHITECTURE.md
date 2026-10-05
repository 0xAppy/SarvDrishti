# SarvDrishti System Architecture

## High-Level Architectural Diagram

```
+-------------------------------------------------------------------------------+
|                             INGESTION SOURCES                                 |
|  1. Live UDP Syslog (Port 5140)   2. Historical Log Files   3. REST API       |
+------------------------------------+------------------------------------------+
                                     |
                                     v
                       +---------------------------+
                       | Apache Kafka (KRaft Mode) |
                       |  Topic: raw-events        |
                       +-------------+-------------+
                                     |
                                     v
                       +---------------------------+
                       | Python Worker Pipeline    |
                       |  1. Format Detection      |
                       |  2. Parser Selection      |
                       |  3. Deterministic Parsing |
                       |  4. Universal Normalizer  |
                       |  5. Validation Engine     |
                       +-------------+-------------+
                                     |
              +----------------------+----------------------+
              |                                             |
              v (Valid / Lossless)                          v (Malformed)
+---------------------------+                 +---------------------------+
| PostgreSQL Data Store     |                 | Apache Kafka Broker       |
| - raw_logs (Raw Payload)  |                 |  Topic: dead-letter-log   |
| - normalized_events (ECS) |                 +---------------------------+
| - field_lineage (Mappings)|
| - parser_registry & audit |
+-------------+-------------+
              |
              v
+---------------------------+
| React Admin Dashboard     |
| - Overview & Live EPS     |
| - Event Explorer & Search |
| - Field Lineage Graph     |
| - AI Onboarding Studio    |
| - Historical File Replay  |
+---------------------------+
```

## Core Component Responsibilities

1. **Ingestion Layer**:
   - Accepts REST API POST requests `/api/events/ingest`.
   - Listens asynchronously on UDP Port 5140 for live Linux Syslog datagrams.
   - Accepts historical log archive files via `/api/replay/upload`.

2. **Buffer & Streaming Layer (Apache Kafka)**:
   - Buffers log bursts to decouple network ingestion from processing workers.
   - Preserves message offsets to support log file replay.

3. **Deterministic Parser Engine & Registry**:
   - `FirewallParser`: Key-Value pair extraction (`SRC=`, `DST=`, `SP=`, `DP=`, `ACTION=`).
   - `SyslogParser`: RFC3164 Syslog header + SSHD authentication pattern parsing.
   - `ApplicationParser`: JSON and KV web access log parsing.
   - `UnknownHeuristicParser`: Tokenization and regex inference for unknown custom logs.

4. **Normalization & Field Lineage Layer**:
   - Standardizes parsed attributes into the Pydantic Universal Schema model.
   - Preserves unmapped fields in `unmapped` dictionary (0% data loss).
   - Generates database records in `field_lineage` linking `normalized_field` -> `raw_field` -> `raw_value` -> `parser_id` -> `raw_id`.

5. **Modular AI Adapter**:
   - Supports OpenAI/Gemini REST APIs, local Ollama models, or offline heuristic rule generation for unknown log onboarding.
   - Operates strictly in the **AI Onboarding Studio** UI view to propose parser rules for human approval.
