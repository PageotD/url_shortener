# test_config.py

import unittest
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
