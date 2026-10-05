# SarvDrishti Universal Common Event Schema

## Schema JSON Specification

```json
{
  "event": {
    "id": "uuid-v4-string",
    "created": "2026-08-26T10:20:16.000000+00:00",
    "category": "network | authentication | web | system | custom_unknown",
    "action": "allow | deny | login_failed | login_success | HTTP GET /login",
    "outcome": "success | failure | unknown"
  },
  "source": {
    "ip": "10.10.1.20",
    "port": 4521
  },
  "destination": {
    "ip": "172.16.2.10",
    "port": 443
  },
  "network": {
    "protocol": "TCP | UDP | ICMP"
  },
  "host": {
    "name": "server01"
  },
  "user": {
    "name": "admin"
  },
  "parser": {
    "id": "firewall-kv-v1",
    "version": "1.0.0"
  },
  "source_id": "src-firewall-01",
  "raw_event_reference": {
    "raw_id": "raw-uuid-v4-string",
    "hash": "sha256-hex-digest-string"
  },
  "unmapped": {
    "vendor_specific_key_1": "value1"
  }
}
```

## Lossless Preservation Guarantee
Any log fields present in the raw event string that do not map directly to core schema attributes (`event`, `source`, `destination`, `network`, `host`, `user`) are automatically retained in the `unmapped` JSON object. No fields are ever discarded.
