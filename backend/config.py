# MARK: Import
# Dependencies
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MARK: EvIELTSConfig
class EvIELTSConfig:
    # MARK: Application
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')