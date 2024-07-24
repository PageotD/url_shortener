# test_keygen.py

import unittest
from shortener_app.keygen import create_random_key
import string

class TestCreateRandomKey(unittest.TestCase):

    def test_default_length(self):
        """Test if the default length of the key is 5 characters."""
        key = create_random_key()
        self.assertEqual(len(key), 5)
        self.assertTrue(all(c in string.ascii_uppercase + string.digits for c in key))

    def test_custom_length(self):
        """Test if a custom length key is generated correctly."""
        length = 10
        key = create_random_key(length)
        self.assertEqual(len(key), length)
        self.assertTrue(all(c in string.ascii_uppercase + string.digits for c in key))

    def test_key_characters(self):
        """Test if the generated key contains only valid characters."""
        key = create_random_key(8)
        self.assertTrue(all(c in string.ascii_uppercase + string.digits for c in key))

    def test_key_uniqueness(self):
        """Test if generated keys are unique across multiple calls."""
        keys = {create_random_key(6) for _ in range(1000)}
        self.assertGreater(len(keys), 950, "Generated keys should be unique")

if __name__ == '__main__':
    unittest.main()
