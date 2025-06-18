# MARK: Import
# Dependencies.
import os
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()

# MARK: EvIELTSConfig
# Configuration class for the Englishvit IELTS API application.
class EvIELTSConfig:
    """
    Configuration class for the Englishvit IELTS API application.

    This class loads configuration values from environment variables and provides
    access to them as class attributes.
    """
    # MARK: Application
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")

    # MARK: OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_whisper_model_name = os.getenv("OPENAI_WHISPER_MODEL_NAME")
    openai_chat_model_name = os.getenv("OPENAI_CHAT_MODEL_NAME")