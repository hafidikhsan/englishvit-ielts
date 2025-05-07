# MARK: Import 
# Dependencies
from flask import Blueprint

# Create a blueprint for the API
api_bp = Blueprint('/api', __name__)

# Routes
from app.api.routes.transcribe import *
from app.api.routes.evaluation import *

# Modules
from app.models.response import EvResponseModel

@api_bp.route('/', methods = ['GET'])
def health():
    return jsonify(EvResponseModel(
        code = 200,
        status = 'Success',
        message = 'Health check successful',
        data = {
            'message': 'API is running',
        }
    ).to_dict()), 200, {'ContentType' : 'application/json'}