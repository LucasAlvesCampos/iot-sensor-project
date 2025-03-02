"""Kafka consumer implementation for sensor data processing."""

from typing import Dict, Any
import json
import logging
from kafka import KafkaConsumer
from .utils.validator import SensorDataValidator
from .utils.db_handler import DatabaseHandler
from .config import KAFKA_CONFIG, MONGO_CONFIG

logger = logging.getLogger(__name__)

class SensorDataConsumer:
    """Consumes and processes sensor data from Kafka."""

    def __init__(self):
        """Initialize consumer with Kafka and MongoDB connections."""
        self.consumer = self._create_consumer()
        self.db_handler = DatabaseHandler(
            MONGO_CONFIG['uri'],
            MONGO_CONFIG['database'],
            MONGO_CONFIG['collection']
        )

    def _create_consumer(self) -> KafkaConsumer:
        """Create and configure Kafka consumer."""
        return KafkaConsumer(
            KAFKA_CONFIG['topic'],
            bootstrap_servers=KAFKA_CONFIG['bootstrap_servers'],
            api_version=KAFKA_CONFIG['api_version'],
            group_id=KAFKA_CONFIG['group_id'],
            auto_offset_reset=KAFKA_CONFIG['auto_offset_reset'],
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )

    def process_message(self, message: Any) -> None:
        """Process a single message from Kafka."""
        try:
            data = message.value
            
            # Validate data structure and types
            is_valid, error_message = SensorDataValidator.validate_data(data)
            if not is_valid:
                logger.warning(f"Invalid message format: {error_message}")
                return

            # Validate value ranges
            is_in_range, range_message, modified_data = (
                SensorDataValidator.validate_value_ranges(data)
            )
            if not is_in_range:             
                logger.warning(f"Value range warning: {range_message} : {modified_data}")

            # Store the validated and modified data
            self.db_handler.store_reading(modified_data)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def run(self) -> None:
        """Start consuming messages."""
        try:
            for message in self.consumer:
                self.process_message(message)
        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        finally:
            self.close()

    def close(self) -> None:
        """Clean up resources."""
        self.consumer.close()
        self.db_handler.close()