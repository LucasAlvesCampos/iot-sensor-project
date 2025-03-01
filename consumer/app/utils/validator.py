"""
Sensor Data Validation Module

This module provides validation functionality for IoT sensor data.
It checks data structure, types, and value ranges for sensor readings.
"""

from typing import Dict, Any, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SensorDataValidator:
    """
    Validator for IoT sensor data.
    
    This class provides static methods to validate sensor data structure,
    data types, and value ranges. It ensures data integrity before storage.

    Attributes:
        REQUIRED_FIELDS (Dict): Mapping of required fields to their expected types
        VALUE_RANGES (Dict): Valid ranges for numeric sensor readings
        
    Example:
        >>> data = {
        ...     'sensor_id': 'Machinery_Sensor_00001',
        ...     'temperature': 25.5,
        ...     'humidity': 60.0,
        ...     'pressure': 1013.25,
        ...     'timestamp': '2025-03-01T12:00:00'
        ... }
        >>> is_valid, message = SensorDataValidator.validate_data(data)
        >>> print(is_valid)
        True
    """

    REQUIRED_FIELDS = {
        'sensor_id': str,
        'temperature': (int, float),
        'humidity': (int, float),
        'pressure': (int, float),
        'timestamp': str
    }

    VALUE_RANGES = {
        'temperature': (-50.0, 100.0),  # Celsius
        'humidity': (0.0, 100.0),       # Percentage
        'pressure': (800.0, 1200.0)     # hPa
    }

    @classmethod
    def validate_data(cls, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates sensor data structure and types.
        
        Checks if all required fields are present with correct types and formats.
        Validates timestamp format and sensor ID structure.
        
        Args:
            data (Dict[str, Any]): Dictionary containing sensor data
                Required keys:
                - sensor_id (str): Format 'Machinery_Sensor_XXXXX'
                - temperature (float/int): Temperature reading
                - humidity (float/int): Humidity reading
                - pressure (float/int): Pressure reading
                - timestamp (str): ISO format timestamp
            
        Returns:
            Tuple[bool, str]: Tuple containing:
                - bool: True if validation passes, False otherwise
                - str: Success or error message
                
        Example:
            >>> data = {'sensor_id': 'Invalid_ID'}
            >>> valid, msg = SensorDataValidator.validate_data(data)
            >>> print(msg)
            'Missing required fields: temperature, humidity, pressure, timestamp'
        """
        try:
            # Check required fields and types
            for field, expected_type in cls.REQUIRED_FIELDS.items():
                if field not in data:
                    return False, f"Missing required field: {field}"
                
                if not isinstance(data[field], expected_type):
                    return False, f"Invalid type for {field}: expected {expected_type}, got {type(data[field])}"

            # Validate timestamp format
            try:
                datetime.fromisoformat(data['timestamp'])
            except ValueError:
                return False, "Invalid timestamp format"

            # Validate sensor_id format
            if not data['sensor_id'].startswith('Machinery_Sensor_'):
                return False, "Invalid sensor_id format"

            return True, "Data validated successfully"

        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False, f"Validation error: {str(e)}"

    @classmethod
    def validate_value_ranges(cls, data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validates sensor value ranges and adds status information.
        
        Checks if numeric values fall within expected ranges and adds validation
        status to the data dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing sensor readings
                Must contain numeric fields:
                - temperature: -50°C to 100°C
                - humidity: 0% to 100%
                - pressure: 800hPa to 1200hPa
            
        Returns:
            Tuple[bool, str, Dict[str, Any]]: Tuple containing:
                - bool: True if all values within range
                - str: Status message
                - Dict: Modified data with validation status
                
        Example:
            >>> data = {'temperature': 150.0}  # Out of range
            >>> valid, msg, modified = SensorDataValidator.validate_value_ranges(data)
            >>> print(modified['status'])
            {'valid': False, 'out_of_range': [{'field': 'temperature', ...}]}
        """
        modified_data = data.copy()
        out_of_range_fields = []

        for field, (min_val, max_val) in cls.VALUE_RANGES.items():
            value = data.get(field)
            if value is not None and not min_val <= value <= max_val:
                out_of_range_fields.append({
                    'field': field,
                    'value': value,
                    'valid_range': f'{min_val} to {max_val}'
                })

        if out_of_range_fields:
            modified_data['status'] = {
                'valid': False,
                'out_of_range': out_of_range_fields
            }
            return False, "Values out of valid ranges", modified_data

        modified_data['status'] = {'valid': True}
        return True, "Values within valid ranges", modified_data

