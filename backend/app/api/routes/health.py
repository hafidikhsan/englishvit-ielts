# MARK: Import
# Dependencies
from flask import jsonify

# Routes
from app.api.routes import api_bp

# Services
from app.services.asr_service import asr_service
from app.services.chat_gpt_service import chatgpt_service

# Modules
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel

# MARK: Health
@api_bp.route('/health', methods = ['GET'])
def health():
    '''
    Health check for the API. This will check if the API is running and
    all the models are loaded successfully.
    '''
    try:
        # Check if the ASR model is loaded
        asr_model = asr_service.health_check()
        chatgpt_model = chatgpt_service.health_check()

        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 200,
                status = 'Success',
                message = 'Health check successful',
            ),
            data = {
                'asr': asr_model,
                'chatgpt': chatgpt_model,
            }
        )

        # Return the health check response
        return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
    
    except Exception as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error in health check',
            ),
            data = {
                'message': 'Internal server error in health check',
                'information': str(error),
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), 500, {'ContentType' : 'application/json'}