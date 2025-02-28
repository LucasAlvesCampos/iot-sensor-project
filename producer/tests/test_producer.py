"""
Test suite for the IoT sensor data producer components.
Tests sensor data generation and Kafka producer functionality.
"""

import pytest
from datetime import datetime
from app.producer import SensorDataProducer
from app.utils.sensor_data_generator import SensorDataGenerator
from kafka.errors import KafkaError

def test_sensor_data_generator():
    """Test if sensor data generator creates valid data structure."""
    generator = SensorDataGenerator()
    data = generator.generate_data()
    
    # Test data structure
    assert isinstance(data, dict), "Generated data should be a dictionary"
    assert all(key in data for key in ['sensor_id', 'temperature', 'humidity', 'pressure', 'timestamp'])

def test_sensor_data_ranges():
    """Test if generated sensor data falls within expected ranges."""
    generator = SensorDataGenerator()
    data = generator.generate_data()
    
    # Test value ranges
    assert 20.0 <= data['temperature'] <= 30.0, "Temperature out of range"
    assert 30.0 <= data['humidity'] <= 70.0, "Humidity out of range"
    assert 980.0 <= data['pressure'] <= 1020.0, "Pressure out of range"

def test_sensor_id_format():
    """Test if sensor IDs follow the expected format."""
    generator = SensorDataGenerator()
    data = generator.generate_data()
    
    assert data['sensor_id'].startswith('Machinery_Sensor_')
    assert len(data['sensor_id']) == 21  # Format: Machinery_Sensor_XXXXX

def test_timestamp_format():
    """Test if timestamp is in valid ISO format."""
    generator = SensorDataGenerator()
    data = generator.generate_data()
    
    try:
        datetime.fromisoformat(data['timestamp'])
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")

@pytest.mark.parametrize("invalid_server", ["", "invalid:port", "localhost:invalid"])
def test_invalid_kafka_connection(invalid_server):
    """Test if producer handles invalid Kafka connections appropriately."""
    with pytest.raises(KafkaError):
        producer = SensorDataProducer(bootstrap_servers=invalid_server, topic="test-topic")

def test_data_types():
    """Test if generated data has correct types."""
    generator = SensorDataGenerator()
    data = generator.generate_data()
    
    assert isinstance(data['sensor_id'], str)
    assert isinstance(data['temperature'], float)
    assert isinstance(data['humidity'], float)
    assert isinstance(data['pressure'], float)
    assert isinstance(data['timestamp'], str)