# SarvDrishti Comprehensive Test Plan

## Test Suite Components

1. **Parser Unit Tests (`test_parsers.py`)**:
   - `test_firewall_parser`: Verifies key-value extraction and unmapped preservation.
   - `test_syslog_parser`: Verifies Linux syslog header and SSHD authentication logic.
   - `test_application_parser`: Verifies web access log and JSON formatting.
   - `test_unknown_heuristic_parser`: Verifies token-based extraction on unknown custom logs.

2. **Lossless Normalization Tests (`test_normalizer.py`)**:
   - `test_lossless_normalizer_firewall`: Checks SHA-256 hash generation, field lineage mappings, and Pydantic schema validation.
   - `test_lossless_normalizer_syslog`: Checks Syslog normalization accuracy.

3. **REST API Integration Tests (`test_api.py`)**:
   - `test_root_endpoint`: Healthcheck assertion.
   - `test_stats_endpoint`: Dashboard system counters assertion.
   - `test_parsers_endpoint`: Registry listing assertion.
   - `test_ingest_and_get_events`: Ingests raw event via REST API and verifies persistence.
   - `test_ai_onboarding_flow`: Tests complete end-to-end sample log analysis, parser validation, and admin approval.

## Execution Command
```bash
PYTHONPATH=backend python3 -m pytest backend/tests -v
```
