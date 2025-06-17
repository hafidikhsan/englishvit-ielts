# MARK: Import
# Dependencies.
from dotenv import load_dotenv
import os

# Load environment variables from .env file.
load_dotenv()

# MARK: EvIELTSConfig
# Configuration class for the EvIELTS application.
class EvIELTSConfig:
    # MARK: Application
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")