"""Flask API for LLM interactions."""
import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from waitress import serve
from core import LLMEngine, load_json_data

load_dotenv()
logger = logging.getLogger(__name__)

# Initialize shared components
engine = LLMEngine()
json_data = load_json_data()

def create_app():
    """Create and configure Flask API application."""
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret')
    
    @app.route('/query', methods=['POST'])
    def query():
        """Handle LLM query and return JSON response."""
        try:
            data = request.get_json()
            if not data or 'prompt' not in data:
                return jsonify({'error': 'Missing prompt in request body'}), 400
            
            prompt = data['prompt'].strip()
            if not prompt:
                return jsonify({'error': 'Prompt cannot be empty'}), 400
            
            response, is_question = engine.query_llm(prompt)
            
            return jsonify({
                'response': response,
                'is_question': is_question,
                'success': True
            })
            
        except Exception as e:
            logger.error(f"Error in API query: {e}")
            return jsonify({'error': 'An error occurred processing the request'}), 500
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({'status': 'healthy', 'service': 'llm-api'})
    
    return app

def start_flask_server():
    """Start the Flask server with waitress."""
    app = create_app()
    port = int(os.getenv('APP_PORT', 5050))
    logger.info(f"Starting Flask API server on port {port}...")
    serve(app, host='0.0.0.0', port=port)