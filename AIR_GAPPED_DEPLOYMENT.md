# SarvDrishti Air-Gapped & Offline Deployment Guide

## Air-Gapped Guarantees

SarvDrishti is engineered to run in 100% air-gapped, isolated military or enterprise security facilities with zero internet connection:

1. **Local Container Services**: PostgreSQL, Apache Kafka, FastAPI Backend, and React Frontend run entirely in local Docker containers.
2. **Deterministic Parsing**: Production streaming requires zero external API calls.
3. **Offline AI Fallback**: If no cloud API key is set, the AI Adapter automatically activates `HeuristicFallbackProvider`, performing offline tokenization and pattern inference on local CPU.
4. **No Remote Dependencies**: All fonts, styling, icons, and JavaScript bundles are built into static assets.

## Verification Command (Air-Gapped Mode)
```bash
# Disconnect internet connection or set mock offline flag
# Run test suite to verify 100% offline functionality
PYTHONPATH=backend python3 -m pytest backend/tests
```
