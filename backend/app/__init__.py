# Import dependencies
import nltk
from flask import Flask
from flask_cors import CORS

# Import modules
from config import EvIELTSConfig
from app.utils.logger import ev_logger

# Import routes
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

    ev_logger.info('Start downloading NLTK models ...')

    # Download and load the NLTK model
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('punkt')
    nltk.download('stopwords')

    ev_logger.info('NLTK models downloaded successfully √')
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix = '/api')


    # Load the ASR model
    ev_logger.info('Start downloading ASR model ...')
    from app.services.asr_service import asr_service
    ev_logger.info('ASR model downloaded successfully √')
    ev_logger.info('Start downloading Spacy model ...')
    from app.services.spacy_service import spacy_service
    ev_logger.info('Spacy model downloaded successfully √')
    ev_logger.info('Start downloading Fluency model ...')
    from app.services.fluency_service import fluency_service
    ev_logger.info('Fluency model downloaded successfully √')
    ev_logger.info('Start downloading Grammar model ...')
    from app.services.grammar_service import grammar_service
    ev_logger.info('Grammar model downloaded successfully √')
    ev_logger.info('Start downloading Lexical model ...')
    from app.services.lexical_service import lexical_service
    ev_logger.info('Lexical model downloaded successfully √')
    ev_logger.info('Start downloading Pronunciation model ...')
    from app.services.pronunciation_service import pronunciation_service
    ev_logger.info('Pronunciation model downloaded successfully √')
    
    # Return the app instance
    return app