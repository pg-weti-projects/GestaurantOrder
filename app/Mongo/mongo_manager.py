import logging
import os

from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

logger = logging.getLogger("app")


class MongoManager:

    def __init__(self):
        username = os.getenv("MONGO_LOGIN")
        password = os.getenv("MONGO_PASSWORD")
        self.url = f"mongodb://{username}:{password}@localhost:27017"
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


    def get_order_list(self):
        return list(self.order_collection.find({}))

    def add_user_record(self, row_data):
        """
            Add a new row of admin input data.
        """
        if "_id" in row_data:
            del row_data["_id"]
        return self.order_collection.insert_one(row_data).inserted_id

    def update_record(self, row_data: dict):
        """
            Update user-entered data.
        """
        object_id = ObjectId(row_data['_id'])
        update_data = {key: value for key, value in row_data.items() if key != "_id"}
        return self.order_collection.update_one({'_id': object_id}, {'$set': update_data})

    def delete_record_from_db(self, dish_id):
        """
            Delete order from database.
        """
        try:
            object_id = ObjectId(dish_id)
            result = self.order_collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error occurred while deleting record: {e}")
            return False
