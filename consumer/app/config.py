"""
Configuration Module

This module provides configuration settings for the Kafka consumer and MongoDB.
Configuration values can be set via environment variables or will use defaults.
"""

from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_CONFIG: Dict[str, Any] = {
    'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'topic': os.getenv('KAFKA_TOPIC', 'sensor-data'),
    'group_id': os.getenv('KAFKA_GROUP_ID', 'sensor-data-consumer'),
    'auto_offset_reset': 'earliest',
    'api_version': tuple(map(int, os.getenv('KAFKA_API_VERSION', '0.10.1').split('.')))
}

MONGO_CONFIG: Dict[str, Any] = {
    'uri': os.getenv('MONGODB_URI', 'mongodb://root:example@mongo:27017/'),
    'database': os.getenv('MONGODB_DATABASE', 'sensor_database'),
    'collection': os.getenv('MONGODB_COLLECTION', 'sensor_data')
}