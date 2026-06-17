import unittest
import json
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""

    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index(self):
        """Test root endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('endpoints', data)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_readiness_check(self):
        """Test readiness check endpoint"""
        response = self.client.get('/ready')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['ready'])

    def test_info_endpoint(self):
        """Test info endpoint"""
        response = self.client.get('/api/v1/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('app_name', data)
        self.assertIn('version', data)

    def test_echo_endpoint(self):
        """Test echo endpoint"""
        test_data = {'message': 'Hello World'}
        response = self.client.post(
            '/api/v1/echo',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['received_data'], test_data)

    def test_echo_endpoint_no_data(self):
        """Test echo endpoint with no data"""
        response = self.client.post(
            '/api/v1/echo',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
