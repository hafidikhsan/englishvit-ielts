# MARK: Import
# Dependencies
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MARK: EvIELTSConfig
class EvIELTSConfig:
    # MARK: Flask
    flask_app = os.getenv('FLASK_APP')
    flask_env = os.getenv('FLASK_ENV', 'production')
    flask_debug = os.getenv('FLASK_DEBUG', 0) == 1
    flask_run_port = os.getenv('FLASK_RUN_PORT', 5000)

    # MARK: AI
    whisper_model = os.getenv('WHISPER_MODEL')
    chatgpt_model = os.getenv('CHATGPT_MODEL')
    openai_api_key = os.getenv('OPENAI_API_KEY')

    # MARK: Audio
    audio_clean_extension = 'wav'
    audio_clean_sample_rate = 16000
    audio_clean_channels = 1

    # MARK: Logging
    log_level = os.getenv('LOG_LEVEL')

    # MARK: Application
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')