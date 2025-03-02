import logging
from time import sleep
from .producer import SensorDataProducer
from .config import KAFKA_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    producer = SensorDataProducer(
        bootstrap_servers=KAFKA_CONFIG['bootstrap_servers'],
        topic=KAFKA_CONFIG['topic']
    )
    
    logger.info("Starting sensor data production...")
    try:
        while True:
            sensor_data = producer.sensor_generator.generate_data()
            producer.send_data(sensor_data)
            sleep(1.0)
    except KeyboardInterrupt:
        logger.info("Shutting down producer...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    main()