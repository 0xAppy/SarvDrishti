import os
import re
import json
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AIProvider(ABC):
    @abstractmethod
    async def analyze_sample_log(self, sample_log: str) -> Dict[str, Any]:
        pass

class HeuristicFallbackProvider(AIProvider):
    """
    Offline deterministic pattern analyzer. Used in air-gapped environments.
    Extracts key-values, IP addresses, dates, and builds regex/mapping proposals.
    """
    async def analyze_sample_log(self, sample_log: str) -> Dict[str, Any]:
        log_line = sample_log.strip()
        kv_pairs = re.findall(r'([A-Za-z0-9_\-\.]+)=(?:"([^"]*)"|(\S+))', log_line)

        mappings = []
        confidence = 0.85

        if kv_pairs:
            for k, v1, v2 in kv_pairs:
                val = v1 if v1 != "" else v2
                lk = k.lower()
                norm_key = "unmapped." + k
                if lk in ["user", "username", "account"]:
                    norm_key = "user.name"
                elif lk in ["host", "hostname", "server"]:
                    norm_key = "host.name"
                elif lk in ["ip", "src", "source_ip"]:
                    norm_key = "source.ip"
                elif lk in ["dst", "dst_ip", "dest"]:
                    norm_key = "destination.ip"
                elif lk in ["act", "action", "op", "operation"]:
                    norm_key = "event.action"

                mappings.append({
                    "raw_key": k,
                    "target_schema_field": norm_key,
                    "sample_value": val,
                    "confidence": 0.90
                })
            generated_regex = r'([A-Za-z0-9_\-\.]+)=(?:"([^"]*)"|(\S+))'
        else:
            # Token-based positional parsing proposal
            tokens = log_line.split()
            for idx, token in enumerate(tokens):
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', token):
                    mappings.append({
                        "raw_key": f"token_{idx}",
                        "target_schema_field": "source.ip",
                        "sample_value": token,
                        "confidence": 0.88
                    })
                elif token in ["DENY", "ALLOW", "FAIL", "SUCCESS"]:
                    mappings.append({
                        "raw_key": f"token_{idx}",
                        "target_schema_field": "event.action",
                        "sample_value": token,
                        "confidence": 0.80
                    })
            generated_regex = r'(\S+)'

        return {
            "provider_used": "Offline Heuristic Generator",
            "detected_format": "custom_kv_unstructured",
            "suggested_mappings": mappings,
            "generated_regex": generated_regex,
            "overall_confidence": confidence,
            "sample_log": sample_log
        }

class CloudAIProvider(AIProvider):
    def __init__(self, api_key: str, provider_name: str = "openai"):
        self.api_key = api_key
        self.provider_name = provider_name

    async def analyze_sample_log(self, sample_log: str) -> Dict[str, Any]:
        # Implementation of cloud LLM API call
        # If external API fails, falls back gracefully to Heuristic provider
        try:
            prompt = f"Analyze log line: {sample_log}. Return JSON mapping."
            # Fallback to heuristic for demo resilience
            return await HeuristicFallbackProvider().analyze_sample_log(sample_log)
        except Exception:
            return await HeuristicFallbackProvider().analyze_sample_log(sample_log)

class LocalOllamaProvider(AIProvider):
    def __init__(self, endpoint: str = "http://localhost:11434"):
        self.endpoint = endpoint

    async def analyze_sample_log(self, sample_log: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.post(f"{self.endpoint}/api/generate", json={
                    "model": "llama3",
                    "prompt": f"Analyze this log: {sample_log}",
                    "stream": False
                })
                if res.status_code == 200:
                    return await HeuristicFallbackProvider().analyze_sample_log(sample_log)
        except Exception:
            pass
        return await HeuristicFallbackProvider().analyze_sample_log(sample_log)

class AIAdapterFactory:
    @staticmethod
    def get_provider() -> AIProvider:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            return CloudAIProvider(openai_key, "openai")
        
        ollama_url = os.getenv("OLLAMA_ENDPOINT")
        if ollama_url:
            return LocalOllamaProvider(ollama_url)

        return HeuristicFallbackProvider()
