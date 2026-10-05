# SIH26156 Requirement Matrix

This matrix evaluates the SarvDrishti project strictly against the official SIH26156 requirements.

| Requirement | Implementation | Code/Component | Demonstration | Status |
| :--- | :--- | :--- | :--- | :--- |
| **a) Preserve complete raw event data without information loss.** | The original payload is saved unaltered in the database alongside normalized fields. | `NormalizedEventDB.raw_payload` | Check database record or UI Event Explorer. | **PASS** |
| **b) Extract and parse source-specific attributes.** | Dedicated regex/KV parsers extract target variables. | `app/parsers/syslog.py`, `firewall.py` | Lineage viewer showing parsed fields. | **PASS** |
| **c) Normalize fields into a common event taxonomy.** | All parsers map their extractions to `UniversalEvent` Pydantic model. | `app/core/schema.py` | Output of `GET /api/events`. | **PASS** |
| **d) Maintain traceability between normalized and original events.** | The `mappings_dict` tracks which raw key populated which universal key. | `EventService.get_lineage()` | Lineage Viewer UI. | **PASS** |
| **e) Plug-and-play onboarding of new log sources.** | The AI Onboarding Studio automatically generates new parsers dynamically. | `OnboardingService.approve_parser()` | Onboarding Studio UI → Approve → Registry. | **PASS** |
| **f) Unified visibility across enterprise environments.** | Aggregated dashboard UI handling Firewall, Web, and Syslog concurrently. | React `Overview.jsx` | Main dashboard view. | **PASS** |
| **g) Efficient SIEM and Data Lake integration.** | REST API exports structured JSON ready for Elastic/Splunk. | `GET /api/events` | cURL command outputting JSON. | **PASS** |
| **h) AI/ML-ready security and operational analytics.** | Normalized schema includes strict typing required for ML training. | `app/core/schema.py` | Code review of Pydantic models. | **PARTIAL** (Data is ready, but no ML analytics engine is actively built in). |
| **i) Reduced parser development effort.** | AI/Heuristic generator creates rules automatically. | `app/ai/adapter.py` | One-click analyze button in Onboarding UI. | **PASS** |
| **j) Deployable in an air-gapped network.** | Core pipeline uses local Python; AI fallback uses local heuristic regex generator. | `HeuristicFallbackProvider` | Running pipeline with internet disabled. | **PASS** |
| **k) May be packaged in a container for platform independence.** | `docker-compose.yml` fully provisions Frontend, Backend, Kafka, and PostgreSQL. | `docker-compose.yml`, `Dockerfile` | `docker compose up --build` | **PASS** |

### Evidence to Show Jury:
*   Show the **Unmapped Fields** section of the Lineage Viewer to prove lossless processing (Requirement A).
*   Demonstrate the **Heuristic Fallback** working offline to prove air-gapped onboarding (Requirement J).
*   Show the `/api/events` JSON output to prove SIEM readiness (Requirement G).

### What NOT to Claim:
*   Do NOT claim the dashboard's "Events/sec" metric is a live Kafka benchmark (it is currently calculated statistically).
*   Do NOT claim the framework *is* a SIEM (it is a pre-processor).
