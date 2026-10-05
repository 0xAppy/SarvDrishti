# SarvDrishti Demo Scripts (SIH26156)

---

## 🎙️ Part 1: Official 2-Minute Spoken Jury Pitch
**Max Time:** 2 Minutes | **Presenter Role:** Team Lead / Speaker

* **0:00 – 0:15 | The Problem**
  > "Enterprise SOCs are drowning in incompatible logs. Firewalls, servers, and custom apps all send data in completely different formats. Security analysts waste thousands of hours just trying to write Regex parsers to make sense of it. We built **SarvDrishti** — the All-Seeing Log Intelligence Engine — to solve this."

* **0:15 – 0:35 | The Ingestion**  
  *(Navigate to `Sources` tab)*
  > "Our framework sits in front of the SIEM. As you can see, we are actively ingesting Enterprise Firewalls via REST, Linux Syslog via a UDP listener on port 5140, and Web App logs. All these radically different formats are pouring into our async queue right now."

* **0:35 – 0:55 | The Normalization**  
  *(Navigate to `Event Explorer`)*
  > "Instantly, our engine intercepts them, applies deterministic parsers, and forces them into a single Universal Schema. Notice how a Cisco firewall log and a Linux auth log both now share the exact same `event.action` and `source.ip` structure. It's ready for any SIEM."

* **0:55 – 1:10 | Lossless Processing**  
  *(Click a firewall event in the Explorer)*
  > "But cybersecurity requires zero data loss. If a firewall sends a weird `VENDOR_MAGIC_ID`, we don't drop it. We preserve the entire raw payload, and gracefully push unknown fields into our `unmapped` JSON bucket. Nothing is lost."

* **1:10 – 1:25 | Field Lineage (Compliance)**  
  *(Navigate to `Lineage Viewer`)*
  > "For legal auditing, we maintain strict provenance. If I click this IP address, the framework traces it backward, proving exactly which raw key it came from, and exactly which version of our parser extracted it."

* **1:25 – 1:45 | Air-Gapped AI Onboarding**  
  *(Navigate to `AI Onboarding`)*
  > "What happens when a completely unknown proprietary log arrives? It gets trapped here. I click 'Analyze', and our fully air-gapped, offline Heuristic AI Adapter instantly reads the string, figures out the schema, and automatically generates a new production Regex parser rule for us. No coding required."

* **1:45 – 2:00 | Scale & Export**
  > "Finally, the system is fully containerized with Kafka and PostgreSQL for infinite scale, and exposes a clean JSON REST API so tools like Splunk can ingest this beautiful, normalized data immediately. Thank you."

---

## 🧪 Part 2: Step-by-Step Interactive Demo Walkthrough
**Purpose:** Technical Validation during Q&A and Jury Deep Dive

1. **Overview & Infrastructure Health**:
   - Open React Dashboard at `http://localhost:3000`.
   - Point out live EPS meter, total processed events, and green status indicators for Kafka, Workers, and PostgreSQL.

2. **Heterogeneous Ingestion (Sources View)**:
   - Navigate to **Sources View**. Show 4 configured sources: Perimeter Firewall (KV), Linux Syslog (UDP 5140), Web App Server (JSON/KV), and Unknown Custom Source.

3. **Event Ingestion & Normalization**:
   - Run `python scripts/generate_logs.py --mode api --count 20`.
   - Switch to **Event Explorer**. Show raw payloads appearing alongside normalized Universal Common Schema JSON records.

4. **Field Lineage & Provenance Demonstration**:
   - Click **View Field Lineage** on a Firewall log event.
   - Show the Lineage Viewer highlighting raw payload key `SRC=10.10.1.20` mapped to normalized field `source.ip` parsed by `firewall-kv-v1`.

5. **AI-Assisted Unknown Source Onboarding**:
   - Navigate to **AI Onboarding Studio**.
   - Input unknown log: `[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL`.
   - Click **Analyze with AI Adapter**. Show AI suggested field mappings and confidence scores.
   - Click **Run Automated Validation**. Show PASS status.
   - Click **Approve & Register Parser**. Show confirmation that the parser is added to the Parser Registry.

6. **Historical Log File Replay**:
   - Navigate to **Historical Replay**.
   - Select `sample_historical.log` generated via `python scripts/generate_logs.py --mode file --count 50`.
   - Click **Start Replay Pipeline**. Show live progress bar streaming lines through Kafka and persisting events into PostgreSQL with lineage.
