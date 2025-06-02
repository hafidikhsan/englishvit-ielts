# MARK: Import 
# Dependencies
from flask import jsonify, Blueprint

# Create a blueprint for the API
api_bp = Blueprint('/api', __name__)
api_v2_bp = Blueprint('/api_v2', __name__)
api_v3_bp = Blueprint('/api_v3', __name__)

# Modules
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel

# Routes
from app.api.routes.evaluation import *
from app.api.routes.health import *
from app.api.routes.information import *
from app.api.routes.overall_feedback import *
from app.api.routes.settings import *
from app.api.routes.transcribe import *

@api_bp.route('/', methods = ['GET'])
def api_base():
    # Define the response model
    response = EvResponseModel(
        metadata = EvResponseMetadataModel(
            code = 200,
            status = 'Success',
            message = 'API check successful',
        ),
        data = {
            'message': 'API is running',
        }
    )
    return jsonify(response.model_dump()), 200, {'ContentType' : 'application/json'}

@api_v2_bp.route('/', methods=['GET'])
def api_v2_base():
    # Define the response model
    response = EvResponseModel(
        metadata = EvResponseMetadataModel(
            code = 200,
            status = 'Success',
            message = 'API V2 check successful',
        ),
        data = {
            'message': 'API V2 is running',
        }
    )
    return jsonify(response.model_dump()), 200, {'ContentType' : 'application/json'}

@api_v3_bp.route('/', methods=['GET'])
def api_v3_base():
    # Define the response model
    response = EvResponseModel(
        metadata = EvResponseMetadataModel(
            code = 200,
            status = 'Success',
            message = 'API V3 check successful',
        ),
        data = {
            'message': 'API V3 is running',
        }
    )
    return jsonify(response.model_dump()), 200, {'ContentType' : 'application/json'}