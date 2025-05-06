# Import dependencies
from flask import Blueprint

# Create a blueprint for the API
api_bp = Blueprint('/api', __name__)

# Import routes
from app.api.routes.transcribe import *

@api_bp.route('/', methods = ['GET'])
def health():
    return jsonify({
        'status' : 'success',
        'message' : 'API is running',
    }), 200, {'ContentType' : 'application/json'}