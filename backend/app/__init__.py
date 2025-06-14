# MARK: Import
# Dependency
from flask import Flask
from flask_cors import CORS

# Modules
from config import EvIELTSConfig
from app.utils.logger import ev_logger

# Routes
from app.api.routes import api_bp, api_v2_bp, api_v3_bp

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
    app.register_blueprint(api_v2_bp, url_prefix = '/api/v2')
    app.register_blueprint(api_v3_bp, url_prefix = '/api/v3')

    # Load the ASR model
    ev_logger.info('Start ASR service ...')
    from app.services.asr_service import asr_service
    ev_logger.info('ASR service successfully started √')
    ev_logger.info('Start ChatGPT service ...')
    from app.services.chat_gpt_service import chatgpt_service
    ev_logger.info('ChatGPT service successfully started √')
    ev_logger.info('Start IELTS service ...')
    from app.services.ielts_services import ielts_service
    ielts_service.update_prompt()
    ev_logger.info('IELTS service successfully started √')
    
    # Return the app instance
    return app