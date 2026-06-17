from flask import Flask, jsonify, request
import logging
import os
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
APP_NAME = os.getenv('APP_NAME', 'Python-K8s-App')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness probe"""
    logger.info('Health check called')
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'app': APP_NAME,
        'version': APP_VERSION
    }), 200


@app.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness check endpoint for Kubernetes readiness probe"""
    logger.info('Readiness check called')
    try:
        return jsonify({
            'ready': True,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f'Readiness check failed: {str(e)}')
        return jsonify({
            'ready': False,
            'error': str(e)
        }), 503


@app.route('/api/v1/info', methods=['GET'])
def get_info():
    """Get application information"""
    logger.info('Info endpoint called')
    return jsonify({
        'app_name': APP_NAME,
        'version': APP_VERSION,
        'environment': ENVIRONMENT,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/api/v1/echo', methods=['POST'])
def echo():
    """Echo endpoint for testing"""
    data = request.get_json()
    logger.info(f'Echo endpoint called with data: {data}')
    
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    return jsonify({
        'message': 'Echo response',
        'received_data': data,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    logger.info('Root endpoint called')
    return jsonify({
        'message': f'Welcome to {APP_NAME}',
        'version': APP_VERSION,
        'endpoints': {
            'health': '/health',
            'ready': '/ready',
            'info': '/api/v1/info',
            'echo': '/api/v1/echo'
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f'404 error: {error}')
    return jsonify({
        'error': 'Endpoint not found',
        'message': str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'500 error: {error}')
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
