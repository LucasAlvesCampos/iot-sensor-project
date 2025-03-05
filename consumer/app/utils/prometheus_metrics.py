from prometheus_client import Counter, Gauge

# Define Prometheus metrics
MESSAGES_PROCESSED = Counter('iot_messages_processed_total', 'Total number of processed messages')
MESSAGES_INVALID = Counter('iot_messages_invalid_total', 'Number of invalid messages')
OUT_OF_RANGE_VALUES = Counter('iot_out_of_range_total', 'Number of out-of-range readings',['parameter', 'sensor_id'])
TEMPERATURE_GAUGE = Gauge('iot_temperature', 'Current temperature reading', ['sensor_id'])
HUMIDITY_GAUGE = Gauge('iot_humidity', 'Current humidity reading', ['sensor_id'])
PRESSURE_GAUGE = Gauge('iot_pressure', 'Current pressure reading', ['sensor_id'])