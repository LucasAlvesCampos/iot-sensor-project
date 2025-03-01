"""Database handling utilities for sensor data storage."""

from typing import Dict, Any, Optional
import logging
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import UpdateResult

logger = logging.getLogger(__name__)

class DatabaseHandler:
    """Handles MongoDB operations for sensor data."""

    def __init__(self, uri: str, database: str, collection: str):
        """
        Initialize database connection and collections.
        
        Args:
            uri: MongoDB connection URI
            database: Database name
            collection: Collection name
        """
        try:
            logger.info(f"Connecting to MongoDB at {uri}")
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db: Database = self.client[database]
            self.collection: Collection = self.db[collection]
            self._setup_indexes()
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def _setup_indexes(self) -> None:
        """Create necessary database indexes."""
        try:
            self.collection.create_index('sensor_id')
            logger.debug("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")
            raise

    def store_reading(self, data: Dict[str, Any]) -> UpdateResult:
        """
        Store sensor reading in MongoDB.
        
        Args:
            data: Validated sensor data to store
            
        Returns:
            UpdateResult: MongoDB update result
            
        Raises:
            Exception: If storage operation fails
        """
        try:
            result = self.collection.update_one(
                {'sensor_id': data['sensor_id']},
                {
                    '$push': {'readings': data},
                    '$setOnInsert': {
                        'sensor_id': data['sensor_id'],
                        'created_at': datetime.utcnow().isoformat()
                    }
                },
                upsert=True
            )
            logger.info(f"Stored data for sensor_id: {data['sensor_id']}")
            return result
        except Exception as e:
            logger.error(f"Error storing data: {e}")
            raise

    def close(self) -> None:
        """Close database connection safely."""
        if hasattr(self, 'client') and self.client:
            try:
                self.client.close()
                logger.info("MongoDB connection closed")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {e}")