import logging
import unittest
from dotenv import load_dotenv
from app.Mongo.mongo_manager import MongoManager

logger = logging.getLogger("app")

class TestMongoDB(unittest.TestCase):
    """
    Test case for MongoDB functionalities using MongoManager.

    This test class verifies various MongoDB operations, including:
        - Connecting to the MongoDB instance
        - Adding items to the MongoDB collection
    """

    def setUp(self):
        """
        Set up the environment for the test.

        This method loads environment variables from the .env file
        and initializes the MongoManager for MongoDB connection.
        """
        load_dotenv()
        self.mongo_manager = MongoManager()

    def test_connection(self):
        """
        Test that verifies the connection to MongoDB is successful.
        """
        try:
            server_info = self.mongo_manager.client.server_info()
            self.assertIsInstance(server_info, dict)
            logger.info("MongoDB connected successfully!")
        except Exception as e:
            self.fail(f"Failed to connect to MongoDB: {str(e)}")

    def test_add_record(self):
        """
        This test adds a new record and validates that it was successfully
        inserted into the collection.
        """
        row_data = {"img_path":"","name": "Pizza", "price": 10.99}
        inserted_id = self.mongo_manager.add_user_record(row_data)

        # Assert that the inserted_id is not None, indicating a successful insert
        self.assertIsNotNone(inserted_id)
        inserted_record = self.mongo_manager.order_collection.find_one({"_id": inserted_id})

        # Assert that the inserted record matches the input data
        self.assertEqual(inserted_record["name"], row_data["name"])
        self.assertEqual(inserted_record["price"], row_data["price"])
        self.assertEqual(inserted_record["img_path"], row_data["img_path"])
        logger.info("Record added and validated successfully!")

    def tearDown(self):
        """
        Cleanup method to ensure the MongoDB connection is closed after each test.
        """
        if self.mongo_manager.client:
            self.mongo_manager.client.close()


if __name__ == '__main__':
    unittest.main()
