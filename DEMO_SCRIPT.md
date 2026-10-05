# SarvDrishti Final Presentation Demo Script (Step-by-Step)

## Demo Sequence for Jury Evaluation

1. **Overview & Infrastructure Health**:
   - Open React Dashboard at `http://localhost:3000`.
   - Point out live EPS meter, total processed events, and green status indicators for Kafka, Workers, and PostgreSQL.

2. **Heterogeneous Ingestion (Sources View)**:
   - Navigate to **Sources View**. Show 4 configured sources: Perimeter Firewall (KV), Linux Syslog (UDP 5140), Web App Server (JSON/KV), and Unknown Custom Source.

3. **Event Ingestion & Normalization**:
   - Run `python3 scripts/generate_logs.py --mode api --count 20`.
   - Switch to **Event Explorer**. Show raw payloads appearing alongside normalized Universal Common Schema JSON records.

4. **Field Lineage & Provenance Demonstration**:
   - Click "View Field Lineage" on a Firewall log event.
   - Show the Lineage Viewer highlighting raw payload key `SRC=10.10.1.20` mapped to normalized field `source.ip` parsed by `firewall-kv-v1`.

5. **AI-Assisted Unknown Source Onboarding**:
   - Navigate to **AI Onboarding Studio**.
   - Input unknown log: `[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL`.
   - Click **Analyze with AI Adapter**. Show AI suggested field mappings and confidence scores.
   - Click **Run Automated Validation**. Show PASS status.
   - Click **Approve & Register Parser**. Show confirmation that the parser is added to the Parser Registry.

6. **Historical Log File Replay**:
   - Navigate to **Historical Replay**.
   - Select `sample_historical.log` generated via `python3 scripts/generate_logs.py --mode file --count 50`.
   - Click **Start Replay Pipeline**. Show live progress bar streaming lines through Kafka and persisting events into PostgreSQL with lineage.
