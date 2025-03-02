# IoT Sensor Data Pipeline API Documentation

## Data Formats

### Sensor Data Format
```json
{
    "sensor_id": "Machinery_Sensor_00001",
    "timestamp": "2025-03-01T12:00:00",
    "temperature": 25.5,
    "humidity": 60.0,
    "pressure": 1013.25
}
```

### Validation Response Format
```json
{
    "sensor_id": "Machinery_Sensor_00001",
    "timestamp": "2025-03-01T12:00:00",
    "temperature": 25.5,
    "humidity": 60.0,
    "pressure": 1013.25,
    "status": {
        "valid": true|false,
        "out_of_range": [
            {
                "field": "temperature",
                "value": 150.0,
                "valid_range": "-50.0 to 100.0"
            }
        ]
    }
}
```

## Validation Rules

### Data Types
- `sensor_id`: string (format: "Machinery_Sensor_XXXXX")
- `timestamp`: string (ISO 8601 format)
- `temperature`: float/integer
- `humidity`: float/integer
- `pressure`: float/integer

### Value Ranges
| Field       | Min    | Max    | Unit |
|-------------|--------|--------|------|
| temperature | -50.0  | 100.0  | °C   |
| humidity    | 0.0    | 100.0  | %    |
| pressure    | 800.0  | 1200.0 | hPa  |

## MongoDB Schema

### Collection: sensor_data
```json
{
    "sensor_id": "Machinery_Sensor_00001",
    "created_at": ISODate("2025-03-01T12:00:00Z"),
    "updated_at": ISODate("2025-03-01T12:00:00Z"),
    "readings": [
        {
            "timestamp": "2025-03-01T12:00:00",
            "temperature": 25.5,
            "humidity": 60.0,
            "pressure": 1013.25,
            "status": {
                "valid": true,
                "out_of_range": []
            }
        }
    ]
}
```

## Query Examples

### Find Invalid Readings
```javascript
db.sensor_data.find({
    "readings.status.valid": false
})
```

### Find High Temperature Readings
```javascript
db.sensor_data.find({
    "readings.temperature": { $gt: 90.0 }
})
```

### Get Reading Count by Sensor
```javascript
db.sensor_data.aggregate([
    { $project: { 
        sensor_id: 1, 
        reading_count: { $size: "$readings" }
    }}
])
```

## Kafka Topics

### sensor_data
- **Purpose**: Raw sensor data streaming
- **Partitions**: 3
- **Replication Factor**: 1
- **Key**: sensor_id
- **Value**: JSON sensor data

## Service URLs

### Development Environment
- Kafka UI: http://localhost:8080
- Mongo Express: http://localhost:8081
- MongoDB: mongodb://localhost:27017

### Connection Parameters
```ini
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=sensor_data
MONGODB_URI=mongodb://root:example@mongo:27017/
```

## Error Handling

### Validation Errors
- Invalid sensor ID format
- Missing required fields
- Invalid data types
- Out of range values

### Processing Errors
- Kafka connection failures
- MongoDB write failures
- Data parsing errors