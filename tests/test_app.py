import unittest
from unittest.mock import patch
from app import app
import json

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

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



if __name__ == "__main__":
    unittest.main()
