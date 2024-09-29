import logging
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

logger = logging.getLogger("app")


class MongoManager:

    def __init__(self):
        self.url = "mongodb://localhost:27017"
        try:
            self.client = MongoClient(self.url)
            self.db = self.client['menu_database']
            self.collection = self.db['menu']
            self.order_collection = self.db['order']
            logger.info("Connected to MongoDB successfully!")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")

    def check_mongo_connection(self) -> bool:
        """
        Performs a ping command on MongoDB client and checks a connection to the database is possible.

        Returns: Returns True if connection is established, False otherwise.
        """
        try:
            self.client.admin.command("ping")
            return True
        except ServerSelectionTimeoutError as e:
            return False