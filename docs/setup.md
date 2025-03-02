# IoT Sensor Project Setup Guide

## Prerequisites

- Windows 10 or later
- Docker Desktop 4.x or later
- Python 3.11+
- Git
- Visual Studio Code

## Development Environment Setup

### 1. Install Required Software

```powershell
# Install Python (if not already installed)
winget install Python.Python.3.11

# Install Docker Desktop
winget install Docker.DockerDesktop

# Install Visual Studio Code
winget install Microsoft.VisualStudioCode
```

### 2. VS Code Extensions

Install the following extensions:
- Python (ms-python.python)
- Docker (ms-azuretools.vscode-docker)
- MongoDB for VS Code (mongodb.mongodb-vscode)

### 3. Clone Repository

```powershell
git clone https://github.com/LucasAlvesCampos/iot-sensor-project.git
cd iot-sensor-project
```

### 4. Python Virtual Environment

```powershell
# Create virtual environments
python -m venv producer/venv
python -m venv consumer/venv

# Activate producer environment
cd producer
.\venv\Scripts\activate
pip install -r requirements.txt

# Activate consumer environment
cd ..\consumer
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Environment Configuration

```powershell
# Copy example environment files
Copy-Item producer/.env.example producer/.env
Copy-Item consumer/.env.example consumer/.env
```

Update the `.env` files with your settings:

```ini
# producer/.env
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=sensor_data
KAFKA_API_VERSION=3.5.1

# consumer/.env
MONGODB_URI=mongodb://root:example@mongodb:27017/
MONGODB_DATABASE=sensor_database
MONGODB_COLLECTION=sensor_data
KAFKA_GROUP_ID=sensor_consumer_group
```

## Docker Setup

### 1. Start Docker Services

```powershell
docker-compose up -d
```

### 2. Verify Services

```powershell
docker-compose ps
```

Expected output:
```
NAME                COMMAND                  SERVICE             STATUS              PORTS
iot-consumer        "python -m app.main"    consumer            running             
iot-producer        "python -m app.main"    producer            running             
kafka               "/opt/bitnami/scri..."   kafka              running             0.0.0.0:9092->9092/tcp
kafka-ui            "/bin/sh -c 'java ..."   kafka-ui           running             0.0.0.0:8080->8080/tcp
mongodb             "docker-entrypoint..."   mongo              running             0.0.0.0:27017->27017/tcp
mongo-express       "tini -- /docker-e..."   mongo-express      running             0.0.0.0:8081->8081/tcp
zookeeper           "/opt/bitnami/scri..."   zookeeper          running             0.0.0.0:2181->2181/tcp
```

## Access Management UIs

- Kafka UI: http://localhost:8080
- Mongo Express: http://localhost:8081

## Running Tests

```powershell
# Run producer tests
cd producer
python -m pytest tests/ -v --cov=app

# Run consumer tests
cd ../consumer
python -m pytest tests/ -v --cov=app
```

## Troubleshooting

### Common Issues

1. **Docker Services Won't Start**
```powershell
# Check logs
docker-compose logs

# Rebuild containers
docker-compose up -d --build
```

2. **MongoDB Connection Issues**
```powershell
# Verify MongoDB is running
docker-compose ps mongo
# Check MongoDB logs
docker-compose logs mongo
```

3. **Kafka Connection Issues**
```powershell
# Check Kafka broker status
docker-compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list
```

### Reset Environment

```powershell
# Stop all containers and remove volumes
docker-compose down -v

# Remove Python cache
Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Recurse -Force

# Restart services
docker-compose up -d
```

## Development Workflow

1. Start services: `docker-compose up -d`
2. Monitor logs: `docker-compose logs -f`
3. Check data in Mongo Express
4. View messages in Kafka UI
5. Stop services: `docker-compose down`