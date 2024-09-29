import logging
from pymongo import MongoClient
from os.path import join, dirname
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
