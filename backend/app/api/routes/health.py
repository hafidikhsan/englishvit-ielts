# MARK: Import
# Dependencies
from flask import jsonify, request

# Routes
from app.api.routes import api_bp

# Services
from app.services.asr_service import asr_service
from app.services.spacy_service import spacy_service
from app.services.grammar_service import grammar_service
from app.services.lexical_service import lexical_service
from app.services.fluency_service import fluency_service

# Modules
from app.models.response_model import EvResponseModel

# MARK: Information
@api_bp.route('/health', methods = ['GET'])
def health():
    '''
    Health check for the API. This will check if the API is running and
    all the models are loaded successfully.
    '''
    try:
        # Check if the ASR model is loaded
        asr_model = asr_service.health_check()
        spacy_model = spacy_service.health_check()
        grammar_model = grammar_service.health_check()
        lexical_model = lexical_service.health_check()
        fluency_model = fluency_service.health_check()

        # Return the health check response
        return jsonify(EvResponseModel(
            code = 200,
            status = 'Success',
            message = 'Health check successful',
            data = {
                'asr': asr_model,
                'spacy': spacy_model,
                'grammar': grammar_model,
                'lexical': lexical_model,
                'fluency': fluency_model
            }
        ).to_dict()), 200, {'ContentType' : 'application/json'}
    
    except Exception as error:
        # Return the error message
        return jsonify(EvResponseModel(
            code = 500,
            status = 'Error',
            message = 'Internal server error in health check',
            data = {
                'error': {
                    'message': str(error),
                },
            },
        ).to_dict()), 500, {'ContentType' : 'application/json'}