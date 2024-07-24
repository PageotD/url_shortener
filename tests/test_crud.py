# test_crud.py

import unittest
from unittest.mock import MagicMock
from shortener_app import crud, models, schemas
from sqlalchemy.orm import Session

class TestCrudOperations(unittest.TestCase):

    def setUp(self):
        # Set up a mock SQLAlchemy session and necessary models/schemas for testing
        self.db = MagicMock(Session)
        self.mock_url = schemas.URLBase(target_url="http://example.com")

    def test_create_db_url(self):
        """Test creating a new URL entry in the database."""
        # Define the expected output
        key = "ABCDE"  # Example fixed key
        secret_key = "12345678"  # Example fixed secret key
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()

        # Mock the keygen function to return predictable values
        with unittest.mock.patch('shortener_app.keygen.create_random_key', side_effect=[key, secret_key]):
            new_url = crud.create_db_url(self.db, self.mock_url)

        self.assertEqual(new_url.target_url, self.mock_url.target_url)
        self.assertEqual(new_url.key, key)
        self.assertEqual(new_url.secret_key, secret_key)
        self.db.add.assert_called_once_with(new_url)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(new_url)

    def test_get_db_url_by_key(self):
        """Test retrieving a URL entry by its key."""
        key = "ABCDE"
        expected_url = models.URL(target_url="http://example.com", key=key, secret_key="12345678")
        self.db.query = MagicMock()
        self.db.query().filter().first = MagicMock(return_value=expected_url)

        result = crud.get_db_url_by_key(self.db, key)

        self.assertEqual(result, expected_url)
        self.db.query().filter().first.assert_called_once()

    def test_get_db_url_by_secret_key(self):
        """Test retrieving a URL entry by its key."""
        key = "ABCDE"
        secret_key = "12345678"
        expected_url = models.URL(target_url="http://example.com", key=key, secret_key=secret_key)
        self.db.query = MagicMock()
        self.db.query().filter().first = MagicMock(return_value=expected_url)

        result = crud.get_db_url_by_secret_key(self.db, key)

        self.assertEqual(result, expected_url)
        self.db.query().filter().first.assert_called_once()

if __name__ == '__main__':
    unittest.main()
