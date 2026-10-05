# Known Limitations & Areas for Future Expansion

This document transparently outlines the current technical limitations of the SarvDrishti prototype. Acknowledging these limitations strengthens the project's defensibility by demonstrating deep engineering awareness.

### 1. Prototype Parser Engine (Regex overhead)
**Limitation:** The current `linux-syslog-v1` and `firewall-kv-v1` parsers rely heavily on standard Python regular expressions (`re` module).
**Impact:** While perfectly sufficient for prototyping and thousands of events per second, Regex can become a CPU bottleneck under extreme load (millions of events per second) and is susceptible to ReDoS (Regular Expression Denial of Service) attacks if poorly formed.
**Future Fix:** Migrate the underlying parsing engine to a high-performance compiled language like Rust (via PyO3 bindings) or utilize optimized Grok/Dissect C-libraries.

### 2. Missing Dedicated Dead Letter Queue (DLQ)
**Limitation:** The current system uses Pydantic to successfully trap validation failures (e.g., malformed IP addresses) and flags them in the SQLite database (`is_valid = false`). However, it does not actively route these failed messages to a dedicated "Dead Letter Queue" Kafka topic for isolated debugging.
**Impact:** Administrators must manually query the database for failed validations rather than having them pushed to an alerting pipeline.
**Future Fix:** Implement a routing layer in `EventService` that pushes `is_valid == false` events back to a dedicated `sarvdrishti-dlq` topic.

### 3. Lack of Role-Based Access Control (RBAC)
**Limitation:** The current React Dashboard and FastAPI backend lack authentication and authorization layers.
**Impact:** Any user on the network can access the dashboard, approve AI-generated parsers, or ingest logs.
**Future Fix:** Implement OAuth2/JWT authentication on the FastAPI routes and create Admin vs. Viewer roles for the UI.

### 4. Limited AI "Self-Healing"
**Limitation:** The system provides "AI-assisted onboarding" by generating regex rules for unknown sources upon manual request. It does not truly "self-heal" by automatically detecting schema drift, generating a new rule in the background, and deploying it without human intervention.
**Impact:** Manual intervention is still required to click "Analyze" and "Approve" in the Onboarding Studio.
**Future Fix:** Build a background cron job that samples the `src-unknown` queue nightly and prepares drafted parsers for admin review.

### 5. In-Memory Statistical Aggregation
**Limitation:** The dashboard's `Events/sec` and `Parsing Success Rate` metrics are calculated via basic database count queries and arbitrary statistical smoothing on the frontend, rather than true real-time stream aggregation.
**Impact:** The metrics are sufficient for a proof-of-concept visualization but would not accurately reflect live micro-second spikes in traffic.
**Future Fix:** Integrate a time-series database (like InfluxDB or Prometheus) and use Kafka Streams for exact windowed aggregations.
