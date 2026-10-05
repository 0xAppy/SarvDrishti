# JURY QA - SarvDrishti Defense Strategy

**1. Why is normalization necessary?**
Because firewalls use `SRC=`, Linux uses `from `, and web apps use `source_ip=`. If a SIEM tries to search for an attacker's IP, it would have to write 30 different queries. Normalization forces them all to `source.ip`, making SIEM queries instant.

**2. Why not send logs directly to SIEM?**
SIEMs charge based on data ingestion volume. If you send messy, unparsed logs, you pay premium prices for raw data storage and waste expensive SIEM CPU cycles parsing it at search-time. SarvDrishti handles this heavy lifting before the SIEM.

**3. Why is SarvDrishti different from Logstash?**
Logstash requires manual coding of complex Grok filters for every new log type. SarvDrishti introduces AI-assisted onboarding, automatically generating the parsing rules for you when an unknown log arrives.

**4. Why is SarvDrishti different from Fluent Bit?**
Fluent Bit is lightweight for edge routing, but lacks compliance-grade Field Lineage and built-in AI parser generation for proprietary enterprise formats.

**5. Why not use Elastic ingest pipelines?**
Vendor lock-in. If you build 500 parsers in Elastic, you can never switch to Splunk. SarvDrishti is vendor-agnostic. We normalize the data to JSON, meaning you can point the output at Elastic today, and Snowflake tomorrow.

**6. Why do you preserve raw logs?**
For legal compliance and chain-of-custody. A normalized field might be parsed incorrectly. The raw payload is the original, legally admissible evidence.

**7. How is lossless processing achieved?**
If a parser encounters a key it doesn't recognize (like a custom `VENDOR_ID`), it doesn't drop it. It places it into an `unmapped` JSON dictionary, ensuring 100% of the original event data is preserved alongside the schema.

**8. How does lineage work?**
Our parsers don't just extract strings; they return a mapping dictionary linking the target schema key (e.g., `source.ip`) directly to the original raw key (e.g., `SRC`), alongside the exact version of the parser used.

**9. How does a new source get onboarded?**
Unknown logs are trapped and sent to the Onboarding Studio. You click 'Analyze', and the AI Adapter reads the tokens, proposes a schema mapping, and generates a Regex pattern. You approve it, and it instantly goes into production.

**10. Why AI?**
Because enterprise networks have hundreds of proprietary, custom-built internal applications. No vendor provides pre-built parsers for custom internal software. AI bridges that gap instantly.

**11. Why doesn't AI process every event?**
Processing 10,000 logs per second with an LLM is too slow and impossibly expensive. The AI is *only* used once to write the Regex rule. The rule is then executed by our lightning-fast deterministic Python engine.

**12. What happens if AI is unavailable?**
We have an air-gapped `HeuristicFallbackProvider` built in. It uses offline deterministic pattern matching to guess IPs, dates, and KV pairs without needing the internet.

**13. How does air-gapped deployment work?**
Our core engine is 100% Python. The message queue, Postgres database, and Heuristic AI parser run entirely offline in Docker containers.

**14. How does the system scale?**
The Python backend pushes raw logs to an asynchronous queue. Multiple background workers pull from this queue concurrently, preventing the REST API from blocking under heavy load.

**15. How would Kafka scale?**
Our `docker-compose.yml` implements Confluent Kafka. If log volume exceeds one machine, Kafka acts as a distributed buffer, allowing us to spin up dozens of horizontally scaled worker containers to consume the topics.

**16. What happens when a worker fails?**
Kafka tracks consumer offsets. If a worker crashes mid-parse, the message is not committed and another worker will automatically pick it up.

**17. What happens when parsing fails?**
The event is still saved to the database. The `parser_id` is marked as `unknown`, and the entire raw string is preserved so it can be replayed later.

**18. What happens to unknown fields?**
Stored safely in the `unmapped` JSON column.

**19. How is schema drift handled?**
If a firewall vendor updates their log format, the parser validation tests will fail. The system will flag the parser, and we can route a sample of the new log to the AI studio to generate an updated `v1.1.0` parser.

**20. How is parser versioning handled?**
Parsers are registered with semantic versioning (`firewall-kv-v1.0.0`). The database records the exact version used for every event to maintain strict lineage accuracy over time.

**21. How do you prevent malicious parser rules?**
AI-generated parsers are never deployed automatically. They must be validated against the sample log, and a human administrator must click "Approve" before they enter the registry.

**22. How do you validate AI-generated parsers?**
The AI proposal is immediately run against the sample log in a sandbox. The validation engine ensures that at least one field was successfully mapped without crashing.

**23. Why SQLite/PostgreSQL?**
SQLite for rapid, zero-dependency laptop prototyping and edge deployments. PostgreSQL (via our Docker compose) for high-concurrency enterprise deployments.

**24. Why asyncio/Kafka?**
Asyncio queues provide instant, zero-latency buffering for local tests. Kafka provides distributed, fault-tolerant message streaming for production.

**25. How would this integrate with Splunk?**
Splunk's HTTP Event Collector (HEC) can be configured to pull directly from our `/api/events` endpoint, ingesting clean JSON.

**26. How would this integrate with Elastic?**
Elasticsearch can ingest our JSON output directly via Logstash or Filebeat configured to poll our API.

**27. How would this integrate with a Data Lake?**
The structured JSON output can be easily written to an S3 bucket or Kafka topic in Parquet format using a simple downstream connector.

**28. What is simulated vs real in the demo?**
The `generate_logs` script generates synthetic strings. However, the `journalctl` streamer runs a live tail on the laptop's actual operating system. The queues, parsers, database, and lineage tracking are 100% real code execution.

**29. What can your current prototype NOT do?**
We do not currently have a dedicated Dead Letter Queue (DLQ) topic in Kafka for routing malformed validations, though the database *does* flag them. We are a pre-processor, not a visualization SIEM.

**30. What would change for billion-event/day deployment?**
We would migrate off the local SQLite onto the Dockerized Kafka/Postgres stack, swap the Python regex engine for Rust-based parsing, and deploy the workers via Kubernetes.
