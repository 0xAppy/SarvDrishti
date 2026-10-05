# SarvDrishti Final Architecture Strategy

Based on the SIH26156 Audit, the SarvDrishti project implements a **Dual-Architecture Strategy** to satisfy both extreme reliability during live laptop demonstrations and true enterprise scalability.

## Architecture A: Current Lightweight Demo Mode (Edge/Local)
*Designed for flawless execution on resource-constrained hardware (e.g., a laptop during a jury presentation).*

*   **Ingestion**: UDP Syslog Listener (Port 5140) & FastAPI REST Endpoint.
*   **Message Broker**: Python `asyncio.Queue` (In-memory, non-blocking).
*   **Workers**: Asyncio task workers executing in the same process footprint as the API.
*   **Database**: SQLite (`sarvdrishti.db`) accessed asynchronously via `aiosqlite`.
*   **AI Engine**: `HeuristicFallbackProvider` (Regex/Pattern matching) functioning entirely offline.

**Why use this for the demo?** 
It eliminates the risk of Docker out-of-memory crashes, port conflicts, or Kafka broker startup failures while standing in front of the jury. It proves the logic works flawlessly.

---

## Architecture B: Enterprise-Scalable Deployment (Data Center)
*Designed for SIH requirements j and k (Air-gapped and Containerized Platform Independence).*

*   **Ingestion**: High-throughput Dockerized Uvicorn workers.
*   **Message Broker**: **Confluent Kafka Broker** (`cp-kafka:7.5.0`) in KRaft mode.
*   **Workers**: Distributed Python consumers reading from Kafka topics.
*   **Database**: **PostgreSQL 15** accessed asynchronously via `asyncpg`.
*   **AI Engine**: `LocalOllamaProvider` (Llama3 running on local GPU cluster).

**How it is implemented:**
This architecture is fully coded and ready to deploy via the existing `docker-compose.yml`. During the jury QA, you can open this file to prove that the Kafka brokers and Postgres schemas are actually implemented, but explain that you are running Architecture A for presentation reliability.

## Downstream SIEM Integration
Both architectures funnel normalized data to the `/api/events` REST endpoint. Downstream tools (Splunk, Elastic, Apache Iceberg) simply poll this endpoint to retrieve heavily structured, normalized, SIH-compliant JSON arrays.
