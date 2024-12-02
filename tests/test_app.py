import unittest
from unittest.mock import patch
from app import app
import json

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True
# 7 Test Cases.
    def test_index(self):
        """Test the index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'IP Information App', response.data)

    def test_about(self):
        """Test the about route"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ABOUT US', response.data)

    def test_fetch_ip_info_ipv4(self):
        """Test the fetch_ip_info API for IPv4"""
        response = self.client.get('/fetch_ip_info?type=ipv4')
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        self.assertIn('ip', response_data)
        self.assertIn('hostname', response_data)
        self.assertIn('city', response_data)
        self.assertIn('region', response_data)
        self.assertIn('country', response_data)

    def test_fetch_ip_info_ipv6(self):
        """Test the fetch_ip_info API for IPv6"""
        response = self.client.get('/fetch_ip_info?type=ipv6')
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        self.assertIn('ip', response_data)
        self.assertIn('hostname', response_data)
        self.assertIn('city', response_data)
        self.assertIn('region', response_data)
        self.assertIn('country', response_data)

    def test_fetch_ip_info_no_type(self):
        """Test the fetch_ip_info API without specifying type (default to ipv4)"""
        response = self.client.get('/fetch_ip_info')
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        self.assertIn('ip', response_data)
        self.assertIn('hostname', response_data)
        self.assertIn('city', response_data)
        self.assertIn('region', response_data)
        self.assertIn('country', response_data)

    @patch('requests.get')  
    def test_fetch_ip_info_error_handling(self, mock_get):
        """Test the fetch_ip_info API when there's a network error"""
        mock_get.side_effect = Exception("Network error")

        response = self.client.get('/fetch_ip_info?type=ipv4')
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'An unexpected error occurred: Network error')

    @patch('requests.get')  
    def test_fetch_ip_info_invalid_ip(self, mock_get):
        """Test the fetch_ip_info API when there's an invalid IP address"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"ip": "invalid_ip"}

        response = self.client.get('/fetch_ip_info?type=ipv4')
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.data)

        
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "Invalid IP address received from the API.")



if __name__ == "__main__":
    unittest.main()
