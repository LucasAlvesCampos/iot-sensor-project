from typing import Dict, Any
import random
from datetime import datetime
from faker import Faker

class SensorDataGenerator:
    """Generate simulated sensor data for IoT devices."""

    def __init__(self):
        """Initialize the sensor data generator with 50 unique sensor IDs."""
        self.sensor_ids = [f'Machinery_Sensor_{i:05d}' for i in range(1, 51)]
        self.faker = Faker()

    def generate_data(self) -> Dict[str, Any]:
        """
        Generate a single sensor data reading.
        
        Returns:
            Dict[str, Any]: A dictionary containing sensor readings with:
                - sensor_id: str
                - timestamp: str (ISO format)
                - temperature: float (°C)
                - humidity: float (%)
                - pressure: float (hPa)
        """
        temperature = round(self.faker.pyfloat(min_value=20.0, max_value=30.0, right_digits=2), 2)
        humidity = round(self.faker.pyfloat(min_value=30.0, max_value=70.0, right_digits=2), 2)
        pressure = round(self.faker.pyfloat(min_value=980.0, max_value=1020.0, right_digits=2), 2)

        return {
            'sensor_id': random.choice(self.sensor_ids),
            'timestamp': datetime.utcnow().isoformat(),
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure
        }