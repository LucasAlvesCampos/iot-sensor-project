from typing import Dict, Any
import random
from datetime import datetime
from faker import Faker

class SensorDataGenerator:
    """Generate simulated sensor data for IoT devices."""

    def __init__(self):
        """Initialize the sensor data generator with 50 unique sensor IDs."""
        self.sensor_ids = [f'Machinery_Sensor_{i:05d}' for i in range(1, 51)]
        self.current_index = 0
        self.faker = Faker()

    def generate_data(self) -> Dict[str, Any]:
        """
        Generate a single sensor data reading with sequential sensor IDs.
        
        Returns:
            Dict[str, Any]: A dictionary containing sensor readings with:
                - sensor_id: str (sequential)
                - timestamp: str (ISO format)
                - temperature: float (°C)
                - humidity: float (%)
                - pressure: float (hPa)
        """
        # Get next sensor ID and increment index
        sensor_id = self.sensor_ids[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.sensor_ids)

        temperature = round(self.faker.pyfloat(min_value=20.0, max_value=30.0, right_digits=2), 2)
        humidity = round(self.faker.pyfloat(min_value=30.0, max_value=70.0, right_digits=2), 2)
        pressure = round(self.faker.pyfloat(min_value=980.0, max_value=1020.0, right_digits=2), 2)

        return {
            'sensor_id': sensor_id,
            'timestamp': datetime.utcnow().isoformat(),
            'temperature': temperature,
            'humidity': humidity,
            'pressure': pressure
        }