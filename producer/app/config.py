"""
Kafka Configuration Module

This module provides configuration settings for the Kafka producer.
Configuration values can be set via environment variables or will use defaults.
"""

from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_CONFIG: Dict[str, Any] = {
    # Kafka broker connection string
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    
    # Topic to publish sensor data
    'topic': os.getenv('KAFKA_TOPIC', 'sensor-data'),
    
    # Kafka API version as tuple (major, minor, patch)
    'api_version': tuple(map(int, os.getenv('KAFKA_API_VERSION', '0.10.1').split('.'))),
    
    # Number of retries if the connection fails
    'retries': int(os.getenv('KAFKA_RETRIES', '3')),
    
    # Producer acknowledgment level ('all' = strongest guarantee)
    'acks': os.getenv('KAFKA_ACKS', 'all'),
    
    # Maximum size of batched messages in bytes
    'batch_size': int(os.getenv('KAFKA_BATCH_SIZE', '16384')),
    
    # Delay in milliseconds for batching
    'linger_ms': int(os.getenv('KAFKA_LINGER_MS', '0')),
    
    # Message compression algorithm
    'compression_type': os.getenv('KAFKA_COMPRESSION', 'gzip'),
    
    # Maximum number of unacknowledged requests
    'max_in_flight_requests_per_connection': int(os.getenv('KAFKA_MAX_IN_FLIGHT', '1'))
}


