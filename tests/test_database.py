import logging
import unittest
from unittest.mock import MagicMock, patch

from bson import ObjectId
from dotenv import load_dotenv
from app.Mongo.mongo_manager import MongoManager

logger = logging.getLogger("app")

class TestMongoDB(unittest.TestCase):
    """
    Test case for MongoDB functionalities using MongoManager.

    This test class verifies various MongoDB operations, including:
        - Connecting to the MongoDB instance
        - Adding items to the MongoDB collection
        - Updating items to the MongoDB collection
        - Deleting items to the MongoDB collection
    """

    def setUp(self):
        """
        Set up the test environment by loading environment variables
        and initializing MongoManager for MongoDB operations.
        """
        load_dotenv()
        self.mongo_manager = MongoManager()

        self.mongo_manager.client = MagicMock()
        self.mongo_manager.db = MagicMock()
        self.mongo_manager.menu_collection = MagicMock()

    @patch('app.Mongo.mongo_manager.MongoClient')
    def test_connection(self, MockMongoClient):
        """
        Test that verifies the connection to MongoDB is successful.
        """
        mock_server_info = {"version": "4.4.3"}
        self.mongo_manager.client.server_info.return_value = mock_server_info
        self.mongo_manager.client.admin.command.return_value = {"ok": 1}

        connection_status = self.mongo_manager.check_mongo_connection()
        self.assertTrue(connection_status)
        logger.info("MongoDB connected successfully!")

    @patch('app.Mongo.mongo_manager.MongoClient')
    def test_read_record(self, MockMongoClient):
        """
        Test that verifies a record can be fetched from the database.
        """
        existing_record = {
            "_id": str(ObjectId()),
            "name": "Pizza",
            "price": 10.99
        }
        self.mongo_manager.menu_collection.find_one = MagicMock(return_value=existing_record)

        fetched_record = self.mongo_manager.get_record_by_id(existing_record["_id"])
        self.assertEqual(fetched_record, existing_record)
        self.mongo_manager.menu_collection.find_one.assert_called_once_with({"_id": ObjectId(existing_record["_id"])})
        logger.info("Record fetched successfully!")

    @patch('app.Mongo.mongo_manager.MongoClient')
    def test_add_record_success(self, MockMongoClient):
        """
        This test adds a new record and validates that it was successfully
        inserted into the collection.
        """
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_id = str(ObjectId())
        self.mongo_manager.menu_collection.insert_one = MagicMock(return_value=mock_insert_result)

        user_data = {"image_path": "", "name": "Pizza", "price": 10.99}
        inserted_id = self.mongo_manager.add_record(user_data)

        # Assert that the inserted_id matches the mock inserted_id
        self.assertEqual(inserted_id, mock_insert_result.inserted_id)
        self.mongo_manager.menu_collection.insert_one.assert_called_once_with(user_data)

        logger.info("User record added and validated successfully!")

    @patch('app.Mongo.mongo_manager.MongoClient')
    def test_update_record(self, MockMongoClient):
        """
        This test update a new record and validates that it was successfully
        inserted into the collection.
        """
        existing_record = {
            "_id": str(ObjectId()),
            "image_path": "",
            "name": "Pizza",
            "price": 10.99
        }

        updated_data = {
            "_id": existing_record["_id"],
            "image_path": "resources/img/dish_img/pizza.png",
            "name": "Pizza Salami",
            "price": 12.99
        }
        mock_update_result = MagicMock()
        mock_update_result.modified_count = 1
        self.mongo_manager.menu_collection.update_one = MagicMock(return_value=mock_update_result)
        result = self.mongo_manager.update_record(updated_data)

        if "_id" in updated_data:
            del updated_data["_id"]

        self.mongo_manager.menu_collection.update_one.assert_called_once_with({"_id": ObjectId(existing_record["_id"])},
                                                                              {"$set": updated_data})
        self.assertEqual(result.modified_count, 1)

        logger.info("User record updated and validated successfully!")

    @patch('app.Mongo.mongo_manager.MongoClient')
    def test_delete_record(self, MockMongoClient):
        """
        Test that verifies deleting a user record from the 'order_collection' in MongoDB.

        This test mocks MongoDB delete_one to prevent real DB operations.
        """
        inserted_id = str(ObjectId())
        user_data = {"image_path": "", "name": "Pizza", "price": 10.99}

        # Mock insert
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_id = inserted_id
        self.mongo_manager.menu_collection.insert_one = MagicMock(return_value=mock_insert_result)
        self.mongo_manager.add_record(user_data)

        mock_delete_result = MagicMock()
        mock_delete_result.deleted_count = 1
        self.mongo_manager.menu_collection.delete_one = MagicMock(return_value=mock_delete_result)

        is_deleted = self.mongo_manager.delete_record(inserted_id)
        self.assertTrue(is_deleted)
        self.mongo_manager.menu_collection.delete_one.assert_called_once_with({"_id": ObjectId(inserted_id)})

        logger.info("User record deleted successfully!")

    def tearDown(self):
        """
        Clean up by closing the MongoDB connection after each test.
        """
        if self.mongo_manager.client:
            self.mongo_manager.client.close()


if __name__ == '__main__':
    unittest.main()
