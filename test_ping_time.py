import unittest
from unittest.mock import patch, MagicMock
from ping_time import ping_request
import requests


class TestStringMethods(unittest.TestCase):


    @patch("builtins.input", return_value="example.com")
    def ping_test(self):
        
        self.assertEqual

if __name__ == '__main__':
    unittest.main()