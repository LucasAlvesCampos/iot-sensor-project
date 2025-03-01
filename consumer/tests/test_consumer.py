"""
Test suite for the IoT sensor data consumer components.
Tests data validation, MongoDB storage, and Kafka consumer functionality.
"""

import pytest
from datetime import datetime
import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from app.consumer import SensorDataConsumer
from app.utils.validator import SensorDataValidator
from app.utils.db_handler import DatabaseHandler
from app.config import MONGO_CONFIG, KAFKA_CONFIG

@pytest.fixture
def valid_sensor_data():
    """Fixture providing valid sensor data."""
    return {
        'sensor_id': 'Machinery_Sensor_00001',
        'timestamp': datetime.utcnow().isoformat(),
        'temperature': 25.5,
        'humidity': 60.0,
        'pressure': 1013.25
    }

@pytest.fixture
def db_handler():
    """Fixture providing a database handler with test database."""
    handler = DatabaseHandler(
        MONGO_CONFIG['uri'],
        'test_database',
        'test_collection'
    )
    yield handler
    # Cleanup after tests
    handler.collection.drop()
    handler.close()

def test_data_validation_valid(valid_sensor_data):
    """Test validation with valid sensor data."""
    is_valid, error = SensorDataValidator.validate_data(valid_sensor_data)
    assert is_valid, f"Validation failed: {error}"
    assert error == "Data validated successfully"

def test_data_validation_invalid():
    """Test validation with invalid sensor data."""
    invalid_data = {
        'sensor_id': 'Invalid_Sensor',
        'temperature': 'not_a_number'
    }
    is_valid, error = SensorDataValidator.validate_data(invalid_data)
    assert not is_valid
    assert error is not None
    assert "Invalid" in error

def test_value_range_validation(valid_sensor_data):
    """Test value range validation."""
    # Test valid ranges
    is_valid, msg, data = SensorDataValidator.validate_value_ranges(valid_sensor_data)
    assert is_valid, msg
    assert data['status']['valid']

    # Test invalid ranges
    invalid_data = valid_sensor_data.copy()
    invalid_data['temperature'] = 150.0
    is_valid, msg, data = SensorDataValidator.validate_value_ranges(invalid_data)
    assert not is_valid
    assert not data['status']['valid']
    assert len(data['status']['out_of_range']) > 0

def test_db_storage(db_handler, valid_sensor_data):
    """Test MongoDB storage functionality."""
    # Store reading
    result = db_handler.store_reading(valid_sensor_data)
    assert result is not None
    
    # Verify storage
    stored_data = db_handler.collection.find_one({'sensor_id': valid_sensor_data['sensor_id']})
    assert stored_data is not None
    assert stored_data['readings'][0]['temperature'] == valid_sensor_data['temperature']
    assert 'created_at' in stored_data

def test_consumer_initialization():
    """Test consumer initialization."""
    try:
        consumer = SensorDataConsumer()
        assert consumer.consumer is not None
        assert consumer.db_handler is not None
    finally:
        if 'consumer' in locals():
            consumer.close()




