# MARK: Import
# Dependencies
import requests
from flask import jsonify, request

# Routes
from app.api.routes import api_bp, api_v2_bp, api_v3_bp

# Services
from app.services.chat_gpt_service import chatgpt_service
from app.services.ielts_services import ielts_service

# Modules
from app.utils.exception import EvClientException, EvAPIException, EvException
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel

# MARK: Evaluation
@api_bp.route('/overall-feedback', methods = ['POST'])
def overall_feedback():
    '''
    Function to handle the overall feedback process.
    '''
    try:
        # Check if the request has a text `session_id`, `finished`, `histories` field
        if 'session_id' not in request.form or 'finished' not in request.form or 'histories' not in request.form:
            # Define the error message
            message = 'Invalid request session_id, finished, and histories are required'

            # Throw an exception
            raise EvClientException(
                message = message,
                information = {
                    'message': message,
                }
            )
        
        # Evaluate using ChatGPT
        result = chatgpt_service.overall_feedback(
            histories = request.form['histories'],
        )

        # Send the result to backend
        if (request.headers.get('Authorization', '') != ''):
            # Define the headers
            headers = {
                'Authorization': request.headers['Authorization'],
            }

            # Define the data
            data = {
                'finished': request.form.get('finished'),
                'overall_band': result.overall.final_band,
                'overall_feedback': result.overall.readable_feedback,
                'fluency_band': result.fluency.final_band,
                'fluency_feedback': result.fluency.readable_feedback,
                'lexical_band': result.lexical.final_band,
                'lexical_feedback': result.lexical.readable_feedback,
                'grammar_band': result.grammar.final_band,
                'grammar_feedback': result.grammar.readable_feedback,
                'pronunciation_band': result.pronunciation.final_band,
                'pronunciation_feedback': result.pronunciation.readable_feedback,
            }

            # Send the request to the Englishvit API
            response = requests.post(
                f"https://englishvit.com/api/user/ielts-ai/session/update/{request.form['session_id']}", 
                data = data, 
                headers = headers,
            )

            # Check if the response is not successful
            if response.status_code != 200:
                # Define the error message
                message = f'Failed to send the evaluation data to the server: {response.text}'

                # Throw an exception
                raise EvAPIException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )

        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 200,
                status = 'Success',
                message = 'Evaluation successful',
            ),
            data = result.model_dump()
        )

        # Return the data
        return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
    
    except EvException as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
            ),
            data = {
                'message': error.message,
                'information': error.information,
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), error.status_code, {'ContentType' : 'application/json'}
    
    except Exception as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error',
            ),
            data = {
                'message': 'Internal server error',
                'information': str(error),
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), 500, {'ContentType' : 'application/json'}
    
@api_v2_bp.route('/overall-feedback', methods = ['POST'])
def overall_feedback():
    '''
    Function to handle the overall feedback process.
    '''
    try:
        # Check if the request has a text `session_id`, `finished`, `histories` field
        if 'session_id' not in request.form or 'finished' not in request.form or 'histories' not in request.form:
            # Define the error message
            message = 'Invalid request session_id, finished, and histories are required'

            # Throw an exception
            raise EvClientException(
                message = message,
            )
        
        # Evaluate using ChatGPT
        result = ielts_service.overall_feedback(
            histories = request.form['histories'],
        )

        # Send the result to backend
        if (request.headers.get('Authorization', '') != ''):
            # Define the headers
            headers = {
                'Authorization': request.headers['Authorization'],
            }

            # Define the data
            data = {
                'finished': request.form.get('finished'),
                'overall_band': result.overall.final_band,
                'overall_feedback': {
                    'feedback': result.overall.readable_feedback,
                    'tips': result.overall.tips_feedback,
                },
                'fluency_band': result.fluency.final_band,
                'fluency_feedback': {
                    'feedback': result.fluency.readable_feedback,
                    'tips': result.fluency.tips_feedback,
                },
                'lexical_band': result.lexical.final_band,
                'lexical_feedback': {
                    'feedback': result.lexical.readable_feedback,
                    'tips': result.lexical.tips_feedback,
                },
                'grammar_band': result.grammar.final_band,
                'grammar_feedback': {
                    'feedback': result.grammar.readable_feedback,
                    'tips': result.grammar.tips_feedback,
                },
                'pronunciation_band': result.pronunciation.final_band,
                'pronunciation_feedback': {
                    'feedback': result.pronunciation.readable_feedback,
                    'tips': result.pronunciation.tips_feedback,
                },
            }

            # Send the request to the Englishvit API
            response = requests.post(
                f"https://englishvit.com/api/user/ielts-ai/session/update/{request.form['session_id']}", 
                data = data, 
                headers = headers,
            )

            # Check if the response is not successful
            if response.status_code != 200:
                # Define the error message
                message = f'Failed to send the evaluation data to the server: {response.text}'

                # Throw an exception
                raise EvAPIException(
                    message = message,
                )

        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 200,
                status = 'Success',
                message = 'Evaluation successful',
            ),
            data = {
                'finished': request.form.get('finished'),
                'overall_band': result.overall.final_band,
                'overall_feedback': {
                    'feedback': result.overall.readable_feedback,
                    'tips': result.overall.tips_feedback,
                },
                'fluency_band': result.fluency.final_band,
                'fluency_feedback': {
                    'feedback': result.fluency.readable_feedback,
                    'tips': result.fluency.tips_feedback,
                },
                'lexical_band': result.lexical.final_band,
                'lexical_feedback': {
                    'feedback': result.lexical.readable_feedback,
                    'tips': result.lexical.tips_feedback,
                },
                'grammar_band': result.grammar.final_band,
                'grammar_feedback': {
                    'feedback': result.grammar.readable_feedback,
                    'tips': result.grammar.tips_feedback,
                },
                'pronunciation_band': result.pronunciation.final_band,
                'pronunciation_feedback': {
                    'feedback': result.pronunciation.readable_feedback,
                    'tips': result.pronunciation.tips_feedback,
                },
            },
        )

        # Return the data
        return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
    
    except EvException as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
            ),
            data = {
                'message': error.message,
                'information': error.information,
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), error.status_code, {'ContentType' : 'application/json'}
    
    except Exception as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error',
            ),
            data = {
                'message': 'Internal server error',
                'information': str(error),
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), 500, {'ContentType' : 'application/json'}
    
@api_v3_bp.route('/overall-feedback', methods = ['POST'])
def overall_feedback():
    '''
    Function to handle the overall feedback process.
    '''
    try:
        # Check if the request has a text `session_id`, `finished`, `histories` field
        if 'session_id' not in request.form or 'finished' not in request.form or 'histories' not in request.form:
            # Define the error message
            message = 'Invalid request session_id, finished, and histories are required'

            # Throw an exception
            raise EvClientException(
                message = message,
            )
        
        # Evaluate using ChatGPT
        result = ielts_service.overall_feedback(
            histories = request.form['histories'],
        )

        # Send the result to backend
        if (request.headers.get('Authorization', '') != ''):
            # Define the headers
            headers = {
                'Authorization': request.headers['Authorization'],
            }

            # Define the data
            data = {
                'finished': request.form.get('finished'),
                'overall_band': result.overall.final_band,
                'overall_feedback': result.overall,
                'fluency_band': result.fluency.final_band,
                'fluency_feedback': result.fluency,
                'lexical_band': result.lexical.final_band,
                'lexical_feedback': result.lexical,
                'grammar_band': result.grammar.final_band,
                'grammar_feedback': result.grammar,
                'pronunciation_band': result.pronunciation.final_band,
                'pronunciation_feedback': result.pronunciation,
            }

            # Send the request to the Englishvit API
            response = requests.post(
                f"https://englishvit.com/api/user/ielts-ai/session/update/{request.form['session_id']}", 
                data = data, 
                headers = headers,
            )

            # Check if the response is not successful
            if response.status_code != 200:
                # Define the error message
                message = f'Failed to send the evaluation data to the server: {response.text}'

                # Throw an exception
                raise EvAPIException(
                    message = message,
                )

        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 200,
                status = 'Success',
                message = 'Evaluation successful',
            ),
            data = {
                'finished': request.form.get('finished'),
                'overall_band': result.overall.final_band,
                'overall_feedback': {
                    'feedback': result.overall.readable_feedback,
                    'tips': result.overall.tips_feedback,
                },
                'fluency_band': result.fluency.final_band,
                'fluency_feedback': {
                    'feedback': result.fluency.readable_feedback,
                    'tips': result.fluency.tips_feedback,
                },
                'lexical_band': result.lexical.final_band,
                'lexical_feedback': {
                    'feedback': result.lexical.readable_feedback,
                    'tips': result.lexical.tips_feedback,
                },
                'grammar_band': result.grammar.final_band,
                'grammar_feedback': {
                    'feedback': result.grammar.readable_feedback,
                    'tips': result.grammar.tips_feedback,
                },
                'pronunciation_band': result.pronunciation.final_band,
                'pronunciation_feedback': {
                    'feedback': result.pronunciation.readable_feedback,
                    'tips': result.pronunciation.tips_feedback,
                },
            },
        )

        # Return the data
        return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
    
    except EvException as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = error.status_code,
                status = 'Error',
                message = error.message,
            ),
            data = {
                'message': error.message,
                'information': error.information,
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), error.status_code, {'ContentType' : 'application/json'}
    
    except Exception as error:
        # Define the response model data
        response_data = EvResponseModel(
            metadata = EvResponseMetadataModel(
                code = 500,
                status = 'Error',
                message = 'Internal server error',
            ),
            data = {
                'message': 'Internal server error',
                'information': str(error),
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), 500, {'ContentType' : 'application/json'}