# MARK: Import
# Dependency
from flask import Flask
from flask_cors import CORS
import threading

# Modules
from config import EvIELTSConfig
from app.utils.logger import ev_logger

# Routes
from app.api.routes import api_bp

# MARK: CreateApp
def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Add more configuration from environment variables
    app.config['DEBUG'] = EvIELTSConfig.flask_debug
    app.config['ENV'] = EvIELTSConfig.flask_env

    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix = '/api')

    # # Load the ASR model
    # ev_logger.info('Start ASR service ...')
    from app.services.asr_service import asr_service
    # ev_logger.info('ASR service successfully started √')
    # # Warm up the model in the background (non-blocking)
    threading.Thread(target=asr_service.get_model, daemon=True).start()
    # ev_logger.info('Start ChatGPT service ...')
    # from app.services.chat_gpt_service import chatgpt_service
    # ev_logger.info('ChatGPT service successfully started √')
    
    # Return the app instance
    return app