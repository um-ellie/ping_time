import unittest
from unittest.mock import patch, MagicMock
from ping_time import ping_request, ping_timer
import requests
import time
import sys
import io

class TestPingRequest(unittest.TestCase):
    """Unit tests for the ping_request function."""

    @patch("builtins.input", return_value="www.example.com")
    @patch("requests.get")
    def test_successful_request(self, mock_get, mock_input):
        """Test a successful HTTP request returns status 200 and correct URL."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.url = "https://www.example.com/"
        mock_response.content = b"Example Domain"
        mock_get.return_value = mock_response

        status, url = ping_request()
        self.assertEqual(status, 200)
        self.assertEqual(url, "https://www.example.com/")

    @patch("builtins.input", return_value="http://redirect.com")
    @patch("requests.get")
    def test_redirect_request(self, mock_get, mock_input):
        """Test a redirect HTTP request returns status 302 and final URL."""
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_response.url = "https://final-destination.com/"
        mock_response.content = b"Redirecting..."
        mock_get.return_value = mock_response

        status, url = ping_request()
        self.assertEqual(status, 302)
        self.assertEqual(url, "https://final-destination.com/")

    @patch("builtins.input", return_value="invalid-url")
    @patch("requests.get", side_effect=requests.RequestException("Invalid URL"))
    def test_invalid_url(self, mock_get, mock_input):
        """Test an invalid URL returns None status and includes the URL in the response."""
        status, url = ping_request()
        self.assertIsNone(status)
        self.assertIn("invalid-url", url)

    @patch("builtins.input", return_value="timeout.com")
    @patch("requests.get", side_effect=requests.exceptions.Timeout("Request timed out"))
    def test_timeout(self, mock_get, mock_input):
        """Test a timeout returns None status and the correct URL."""
        status, url = ping_request()
        self.assertIsNone(status)
        self.assertEqual(url, "https://timeout.com/")

    @patch("builtins.input", return_value="unreachable.com")
    @patch("requests.get", side_effect=requests.ConnectionError("Failed to connect"))
    def test_unreachable(self, mock_get, mock_input):
        """Test an unreachable host returns None status and the correct URL."""
        status, url = ping_request()
        self.assertIsNone(status)
        self.assertEqual(url, "https://unreachable.com/")

class TestPingTimer(unittest.TestCase):
    """Unit tests for the ping_timer decorator."""

    def test_ping_timer_execution_time(self):
        """Test that ping_timer prints execution time and returns function result."""

        @ping_timer
        def slow_function():
            time.sleep(1)
            return "Completed"

        # Capture the output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        result = slow_function()

        # Restore stdout
        sys.stdout = sys.__stdout__

        self.assertEqual(result, "Completed")
        output = captured_output.getvalue()
        self.assertIn("Request completed in", output)

        # Extract the ms value after 'OR'
        ms_part = output.split("OR")[1].split("ms")[0].strip()
        reported_time = float(ms_part)
        self.assertGreater(reported_time, 0)

if __name__ == '__main__':
    unittest.main()