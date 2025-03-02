# IoT Sensor Data Pipeline

A distributed system for collecting, validating, and storing IoT sensor data using Apache Kafka and MongoDB.

## Project Overview

This project implements a scalable data pipeline for IoT sensor data with the following components:
- Data Producer: Generates simulated sensor readings
- Kafka Message Queue: Handles data streaming
- Data Consumer: Validates, processes and stores sensor readings
- MongoDB: Persistent storage for sensor data

## Architecture

```ascii
┌──────────────┐    ┌───────┐    ┌──────────────┐    ┌──────────┐
│   Producer   │───►│ Kafka │───►│   Consumer   │───►│ MongoDB  │
│(Python/Faker)│    │       │    │(Validation)  │    │          │
└──────────────┘    └───────┘    └──────────────┘    └──────────┘
```

## Features

- Sequential sensor ID generation
- Realistic sensor data simulation
- Data validation and range checking
- Scalable message queue system
- Persistent storage with MongoDB
- Docker containerization
- Monitoring interfaces (Kafka UI, Mongo Express)

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/LucasAlvesCampos/iot-sensor-project.git

cd iot-sensor-project

2. Create environment files:

cp producer/.env.example producer/.env
cp consumer/.env.example consumer/.env

3. Start the serice

docker-compose up -d

4.Monitor the services:

Kafka UI: http://localhost:8080
Mongo Express: http://localhost:8081