from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class BaseParser(ABC):
    """
    Abstract Base Class for all ULPF Log Parsers.
    Every parser must declare parser_id, version, format, and return:
    - extracted_fields: Dict of standardized normalized field keys and values
    - raw_field_mapping: Dict mapping normalized field key -> original raw token key
    - unmapped_fields: Dict of any raw fields that did not map to core standard fields
    """
    parser_id: str = "base-parser"
    version: str = "1.0.0"
    format_name: str = "generic"

    @abstractmethod
    def parse(self, raw_payload: str) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
        pass
