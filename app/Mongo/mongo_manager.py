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
            self.menu_collection = self.db['menu']
            logger.info("Connected to MongoDB successfully!")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")

    def add_record(self, row_data: dict):
        """
            Add a new row of admin input data.
        """
        if "_id" in row_data:
            del row_data["_id"]
        return self.menu_collection.insert_one(row_data).inserted_id

    def update_record(self, row_data: dict):
        """
            Update user-entered data.
        """
        object_id = ObjectId(row_data['_id'])
        update_data = {key: value for key, value in row_data.items() if key != "_id"}
        return self.menu_collection.update_one({'_id': object_id}, {'$set': update_data})

    def delete_record(self, dish_id: str):
        """
            Delete record from database by dish_id.
        """
        try:
            object_id = ObjectId(dish_id)
            result = self.menu_collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error with deleting record: {e}")
            return False

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
        return list(self.menu_collection.find({}))

    def get_dish_by_id(self, dish_id):
        """
            Get all dish data from the database by its ID.
        """
        return self.menu_collection.find_one({"_id": ObjectId(dish_id)})
