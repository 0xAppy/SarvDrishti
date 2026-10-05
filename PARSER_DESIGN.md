# SarvDrishti Parser Design & Registry Specification

## Parser Architecture

All parsers inherit from `BaseParser` in `backend/app/parsers/base.py`:

```python
class BaseParser(ABC):
    parser_id: str
    version: str
    format_name: str

    @abstractmethod
    def parse(self, raw_payload: str) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
        """
        Returns:
          1. extracted_fields (Dict of normalized schema key -> extracted value)
          2. raw_field_mapping (Dict of normalized schema key -> raw token key)
          3. unmapped_fields (Dict of unmapped raw vendor fields)
        """
        pass
```

## Production Parsers Included

1. **`firewall-kv-v1`**: Key-Value parser for perimeter firewall logs (`SRC`, `DST`, `SP`, `DP`, `PROTO`, `ACTION`).
2. **`linux-syslog-v1`**: RFC3164 Syslog header & SSHD authentication parser (`timestamp`, `host`, `user`, `from_ip`).
3. **`web-application-v1`**: JSON and Key-Value web server access log parser (`method`, `path`, `status`, `source_ip`).
4. **`unknown-heuristic-v1`**: Offline regex & tokenization parser for unformatted custom vendor logs.
5. **AI-Generated Dynamic Parsers**: Created on the fly via the AI Onboarding Studio and saved into PostgreSQL.
