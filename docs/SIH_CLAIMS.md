# SIH26156 Claims Strategy — Team Black Pearl

When presenting SarvDrishti to the jury, use this strict guide to ensure all technical claims are defensible and directly backed by the existing repository.

## 🟢 SAFE CLAIMS
*Say these with total confidence. They are 100% implemented.*

*   "SarvDrishti successfully ingests heterogeneous log formats concurrently (Syslog, REST, Historical)."
*   "We normalize unstructured data into a rigid Universal Schema."
*   "We preserve 100% of the raw event data."
*   "Our Field Lineage system proves exactly which parser extracted which field."
*   "Unrecognized vendor-specific keys are gracefully preserved in an `unmapped` dictionary."
*   "The core pipeline is completely functional in an air-gapped, offline environment."
*   "Our Heuristic AI fallback generator can build Regex rules offline without a cloud LLM."
*   "Our API exports clean, SIEM-ready JSON output."

## 🟡 PARTIAL CLAIMS
*Use careful phrasing. These are architecturally designed but not fully implemented to enterprise scale in the live demo.*

*   **"Designed for horizontal scaling."** *(Safe phrasing: "The architecture isolates ingestion from parsing via an asynchronous queue, allowing us to spin up multiple distributed workers when deployed via our included Docker Compose Kafka stack.")*
*   **"AI-Assisted Self-Healing."** *(Safe phrasing: "When unknown logs arrive, they are trapped. The AI assists the administrator by generating the complex regex rule automatically, reducing onboarding time from hours to seconds.")*
*   **"Validation & Error Handling."** *(Safe phrasing: "Pydantic immediately flags malformed fields like invalid IPs in the database, ensuring bad data is audited rather than silently dropped.")*

## 🔴 DO NOT CLAIM
*If the jury asks about these, admit they are limitations. Do not pretend they are implemented.*

*   **"Processes billions of events/day."** *(Instead say: "The prototype handles thousands of events per second on a laptop. To hit a billion a day, we would deploy our Dockerized Kafka broker and scale Kubernetes workers.")*
*   **"Fully Autonomous Self-Healing."** *(Do not claim the AI automatically fixes live streams without human approval. We explicitly require human validation for security).*
*   **"We built our own SIEM."** *(Instead say: "We built the preprocessing pipeline that feeds a SIEM. We make Splunk cheaper and faster.")*
*   **"Real-Time Metrics."** *(Do not claim the dashboard throughput numbers are live streaming aggregations; admit they are UI approximations based on database counts).*
