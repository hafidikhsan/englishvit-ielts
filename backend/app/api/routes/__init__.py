# MARK: Import 
# Dependencies
from flask import jsonify, Blueprint

# Create a blueprint for the API
api_bp = Blueprint('/api', __name__)

# Modules
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel

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
    return jsonify(response.json()), 200, {'ContentType' : 'application/json'}