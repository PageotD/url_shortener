# test_config.py

import unittest
from unittest.mock import patch
from shortener_app.config import Settings, get_settings

class TestSettings(unittest.TestCase):
    def test_default_settings(self):
        """
        Test that the default settings are loaded correctly.
        """
        settings = Settings()
        self.assertEqual(settings.env_name, "Local")
        self.assertEqual(settings.base_url, "http://localhost:8000")
        self.assertEqual(settings.db_url, "sqlite:///./shortener.db")

    @patch.dict('os.environ', {'ENV_NAME': 'Production', 'BASE_URL': 'https://prod.example.com', 'DB_URL': 'postgresql://user:password@localhost/prod_db'})
    def test_env_variables(self):
        """
        Test that the settings are correctly loaded from environment variables.
        """
        settings = Settings()
        self.assertEqual(settings.env_name, "Production")
        self.assertEqual(settings.base_url, "https://prod.example.com")
        self.assertEqual(settings.db_url, "postgresql://user:password@localhost/prod_db")

    @patch.dict('os.environ', {'ENV_NAME': 'Staging'})
    def test_partial_env_variables(self):
        """
        Test that partial environment variables are correctly applied, falling back to defaults.
        """
        settings = Settings()
        self.assertEqual(settings.env_name, "Staging")
        self.assertEqual(settings.base_url, "http://localhost:8000")
        self.assertEqual(settings.db_url, "sqlite:///./shortener.db")

    def test_get_settings(self):
        """
        Test that the get_settings function returns the correct settings.
        """
        settings = get_settings()
        self.assertIsInstance(settings, Settings)
        self.assertEqual(settings.env_name, "Local")
        self.assertEqual(settings.base_url, "http://localhost:8000")
        self.assertEqual(settings.db_url, "sqlite:///./shortener.db")

if __name__ == '__main__':
    unittest.main()
