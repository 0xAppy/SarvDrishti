import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("sarvdrishti.kafka.producer")

# In-memory queue fallback when Kafka is not available
in_memory_queue: list = []

class EventProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self._producer = None
        self._is_kafka_connected = False

    def connect(self):
        try:
            from kafka import KafkaProducer
            self._producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=2000,
                max_block_ms=2000
            )
            self._is_kafka_connected = True
            logger.info(f"Connected to Kafka broker at {self.bootstrap_servers}")
        except Exception as e:
            self._is_kafka_connected = False
            logger.warning(f"Kafka connection failed ({e}). Falling back to in-memory event stream.")

    def send_raw_event(self, raw_payload: str, source_id: str = "src-default", topic: str = "raw-events") -> bool:
        message = {
            "raw_payload": raw_payload,
            "source_id": source_id
        }
        if self._is_kafka_connected and self._producer:
            try:
                self._producer.send(topic, value=message)
                return True
            except Exception as e:
                logger.error(f"Failed to produce message to Kafka: {e}")

        # Fallback in-memory queuing
        in_memory_queue.append(message)
        return True

producer = EventProducer()
