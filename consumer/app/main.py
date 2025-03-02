"""Main entry point for the sensor data consumer service."""

import logging
from .consumer import SensorDataConsumer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Start the consumer service."""
    try:
        consumer = SensorDataConsumer()
        logger.info("Starting sensor data consumer...")
        consumer.run()
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    except Exception as e:
        logger.error(f"Error running consumer: {e}")
        raise

if __name__ == "__main__":
    main()