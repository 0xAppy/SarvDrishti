# SarvDrishti AI Onboarding & Modular Adapter Architecture

## Decoupled AI Layer Design

SarvDrishti strictly decouples log streaming from the AI layer:
- **Production Streaming**: Parsed 100% deterministically using compiled Python rules (thousands of logs/sec).
- **AI Module**: Invoked **ONLY** for unknown log source onboarding.

```
Unknown Log Sample
        |
        v
AI Adapter Interface (Cloud API / Local Ollama / Offline Heuristic)
        |
        v
Suggested Mappings & Regex Generation
        |
        v
Automated Validation Engine (PASS/FAIL)
        |
        v
Human Administrator Review & Approval
        |
        v
Registered Deterministic Production Parser
```

## AI Adapter Providers

1. **`CloudAIProvider`**: Uses OpenAI or Gemini API when API keys are configured.
2. **`LocalOllamaProvider`**: Connects to local Ollama instance (`http://localhost:11434`) for local LLM execution.
3. **`HeuristicFallbackProvider`**: Fully offline token & pattern analyzer for 100% air-gapped operation without internet or GPU.
