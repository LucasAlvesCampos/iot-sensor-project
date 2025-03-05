# IoT Sensor Data Pipeline

A distributed system for collecting, validating, and storing IoT sensor data using Apache Kafka, MongoDB, Prometheus, and Grafana.

## Project Overview

This project implements a scalable data pipeline for IoT sensor data with the following components:
- Data Producer: Generates simulated sensor readings
- Kafka Message Queue: Handles data streaming
- Data Consumer: Validates, processes and stores sensor readings
- MongoDB: Persistent storage for sensor data
- Prometheus: Metrics collection and monitoring
- Grafana: Data visualization and alerting

## Architecture

```ascii
┌──────────────┐    ┌───────┐    ┌──────────────┐    ┌──────────┐
│   Producer   │───►│ Kafka │───►│   Consumer   │───►│ MongoDB  │
│(Python/Faker)│    │       │    │(Validation)  │    │          │
└──────────────┘    └───────┘    └──────────────┘    └──────────┘
                                        │
                                        ▼
                                 ┌──────────────┐    ┌──────────┐
                                 │  Prometheus  │───►│ Grafana  │
                                 │  (Metrics)   │    │(Dashoard)│
                                 └──────────────┘    └──────────┘
```

## Features

- Sequential sensor ID generation
- Realistic sensor data simulation
- Data validation and range checking
- Scalable message queue system
- Persistent storage with MongoDB
- Docker containerization
- UI interfaces for better troubleshooting (Kafka UI, Mongo Express)
- Metrics collecting
- Data visualization dashboards and alerts

## Components

### Data Storage
- **MongoDB**: Primary database for sensor readings
  - Credentials: root/example
  - Port: 27017
  - Web Interface: http://localhost:8081 (Mongo Express)

### Message Queue
- **Apache Kafka**: Message broker for data streaming
  - Bootstrap Server: kafka:9092
  - Zookeeper: zookeeper:2181
  - Web Interface: http://localhost:8080 (Kafka UI)
  - Partitions: 3

### Monitoring
- **Prometheus**: Metrics collection
  - Web Interface: http://localhost:9090
  - Scrape interval: 15s
  - Metrics endpoint: http://consumer:8000/metrics

- **Grafana**: Data visualization
  - Web Interface: http://localhost:3000
  - Default credentials: admin/admin
  - Features:
    - Custom dashboards
    - Alert configuration
    - Multi-source support

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

## Available Metrics

### Consumer Metrics
- `iot_messages_processed_total`: Total processed messages
- `iot_messages_invalid_total`: Invalid message count
- `iot_out_of_range_total`: Out-of-range readings by parameter and sensor_id
- `iot_temperature`: Current temperature readings by sensor_id
- `iot_humidity`: Current humidity readings by sensor_id
- `iot_pressure`: Current pressure readings by sensor_id

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/LucasAlvesCampos/iot-sensor-project.git
```

2. Enter project directory
```bash
cd iot-sensor-project
```

3. Create environment files:
```bash
cp producer/.env.example producer/.env
cp consumer/.env.example consumer/.env
```

3. Start the services
```bash
docker-compose up -d
```

4. Access the interfaces:
- Kafka UI: http://localhost:8080
- Mongo Express: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Monitoring Setup

1. **Configure Prometheus Data Source in Grafana**:
   - URL: http://prometheus:9090
   - Access: Server (default)

2. **Create Dashboards for**:
   - Message processing rates
   - Invalid message counts
   - Out-of-range values
   - Current sensor readings

3. **Set Up Alerts for**:
   - High temperature readings
   - Invalid message spikes
   - Out-of-range value patterns
