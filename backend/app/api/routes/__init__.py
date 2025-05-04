# Import dependencies
from flask import Blueprint

# Create a blueprint for the API
api_bp = Blueprint('/api', __name__)

# Import routes
from app.api.routes.transcribe import *
