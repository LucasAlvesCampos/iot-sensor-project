from typing import Dict, Any, Optional
import json
import logging

from kafka import KafkaProducer
from kafka.errors import KafkaError

from .config import KAFKA_CONFIG
from .utils.sensor_data_generator import SensorDataGenerator

logger = logging.getLogger(__name__)

class SensorDataProducer:
    """Handles production of sensor data to Kafka topics."""

    def __init__(self, bootstrap_servers: str, topic: str):
        """
        Initialize the sensor data producer.

        Args:
            bootstrap_servers (str): Comma-separated list of Kafka broker URLs
            topic (str): Kafka topic to produce messages to

        Raises:
            KafkaError: If producer creation fails
        """
        self.topic = topic
        self.producer: Optional[KafkaProducer] = None
        self.sensor_generator = SensorDataGenerator()
        self.producer = self._create_producer(bootstrap_servers)

    def _create_producer(self, bootstrap_servers: str) -> KafkaProducer:
        """
        Create and configure a Kafka producer instance.

        Args:
            bootstrap_servers (str): Comma-separated list of Kafka broker URLs

        Returns:
            KafkaProducer: Configured Kafka producer instance

        Raises:
            KafkaError: If producer creation fails
        """
        try:
            return KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                api_version=KAFKA_CONFIG['api_version'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=KAFKA_CONFIG['retries'],
                acks=KAFKA_CONFIG['acks']
            )
        except KafkaError as ke:
            logger.error(f"Failed to create Kafka producer: {ke}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating producer: {e}")
            raise

    def send_data(self, data: Dict[str, Any]) -> None:
        """
        Send sensor data to Kafka topic.

        Args:
            data (Dict[str, Any]): Sensor data to send

        Raises:
            KafkaError: If sending fails
            ValueError: If producer is not initialized
        """
        if not self.producer:
            raise ValueError("Producer not initialized")

        try:
            future = self.producer.send(
                self.topic,
                value=data,
                key=data['sensor_id']
            )
            # Wait for the message to be delivered
            record_metadata = future.get(timeout=10)
            logger.info(
                f"Message sent to {record_metadata.topic}:"
                f"partition={record_metadata.partition},"
                f"offset={record_metadata.offset}"
            )
        except KafkaError as ke:
            logger.error(f"Failed to send message: {ke}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")
            raise

    def close(self) -> None:
        """
        Cleanly shut down the producer.
        
        This method should be called when the producer is no longer needed.
        """
        if self.producer:
            try:
                self.producer.flush()  # Ensure all messages are sent
                self.producer.close()
                logger.info("Producer closed successfully")
            except Exception as e:
                logger.error(f"Error closing producer: {e}")
                raise
            finally:
                self.producer = None