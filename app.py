from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set environment variables for API keys
ONET_API_KEY = 'Basic dml0dXJhbHZvY2F0aW9udmVudHU6NjM4NXJ4ZQ=='
ONET_BASE_URL = 'https://services.onetcenter.org/ws/online/v1/'


@app.route('/api/careers/search', methods=['POST'])
def search_careers():
    try:
        criteria = request.get_json()
        if not criteria:
            return jsonify({'error': 'No search criteria provided'}), 400

        headers = {
            'Authorization': ONET_API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        logger.info("Search criteria: %s", criteria)

        response = requests.post(
            f'{ONET_BASE_URL}/careers/search',
            headers=headers,
            json=criteria,
            timeout=10
        )

        logger.info("Career Search Response Status: %d", response.status_code)
        logger.info("Response content: %s", response.text)

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        logger.error("Error in career search request: %s", str(e))
        return jsonify({'error': f"API request failed: {str(e)}"}), 500
    except json.JSONDecodeError as e:
        logger.error("JSON decode error: %s", str(e))
        return jsonify({'error': 'Invalid response format'}), 500
    except Exception as e:
        logger.error("Error searching careers: %s", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/onet/occupation', methods=['GET'])
def get_occupation_data():
    try:
        headers = {
            'Authorization': ONET_API_KEY,
            'Accept': 'application/json'
        }

        response = requests.get(
            f'{ONET_BASE_URL}/occupation/sample',
            headers=headers,
            timeout=10
        )

        logger.info("O*NET API Response Status: %d", response.status_code)
        logger.info("Response content: %s", response.text)

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        logger.error("API request error: %s", str(e))
        return jsonify({'error': f"API request failed: {str(e)}"}), 500
    except Exception as e:
        logger.error("Error fetching O*NET data: %s", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    if not ONET_API_KEY:
        return jsonify({
            'status': 'unhealthy',
            'error': 'API key is missing',
            'details': 'O*NET API key is not configured'
        }), 500

    try:
        headers = {
            'Authorization': ONET_API_KEY,
            'Accept': 'application/json'
        }

        test_response = requests.get(
            f'{ONET_BASE_URL}/occupation/sample',
            headers=headers,
            timeout=5
        )

        if test_response.status_code == 200:
            return jsonify({
                'status': 'healthy',
                'api_key_present': True,
                'api_connection': 'successful',
                'response_code': test_response.status_code
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'api_key_present': True,
                'api_connection': 'failed',
                'response_code': test_response.status_code
            }), 500

    except Exception as e:
        logger.error("Health check failed: %s", str(e))
        return jsonify({
            'status': 'unhealthy',
            'api_key_present': True,
            'error': str(e),
            'details': 'Failed to connect to O*NET API'
        }), 500


if __name__ == '__main__':
    try:
        # Server startup logging
        api_key_status = 'present' if ONET_API_KEY else 'missing'
        logger.info('==============================================')
        logger.info('Server Startup Configuration:')
        logger.info('O*NET API key status: %s', api_key_status)
        logger.info('Server URL: http://0.0.0.0:5000')
        logger.info('Debug mode: enabled')
        logger.info('CORS: enabled')
        logger.info('API Base URL: %s', ONET_BASE_URL)
        logger.info('==============================================')

        # Optional: Test API connection at startup
        if ONET_API_KEY:
            test_headers = {
                'Authorization': ONET_API_KEY,
                'Accept': 'application/json'
            }
            test_response = requests.get(
                f'{ONET_BASE_URL}/occupation/sample',
                headers=test_headers,
                timeout=5
            )
            logger.info('API Connection Test: %s',
                        'SUCCESS' if test_response.status_code == 200 else 'FAILED')
            logger.info('API Response Status: %d', test_response.status_code)

        # Start Flask server
        print('Server starting on port 5000...')
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True,
            threaded=True
        )

    except Exception as e:
        logger.error('Server startup failed: %s', str(e))
        print('Error starting server: %s' % str(e))
        raise
