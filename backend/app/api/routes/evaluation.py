# MARK: Import
# Dependencies
import requests
from flask import jsonify, request

# Routes
from app.api.routes import api_bp

# Services
from app.services.chat_gpt_service import chatgpt_service

# Modules
from app.utils.exception import EvClientException, EvAPIException, EvException
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel

# MARK: Evaluation
@api_bp.route('/evaluation', methods = ['POST'])
def evaluation():
    '''
    Function to handle the evaluation process.
    '''
    try:
        # Check if the request has a text `question`, `answer`, `confidence` and `test_id` field
        if 'question' not in request.form or 'answer' not in request.form or 'confidence' not in request.form or 'test_id' not in request.form:
            # Define the error message
            message = 'Invalid request, question, answer, confidence, and test_id are required'

            # Throw an exception
            raise EvClientException(
                message = message,
                information = {
                    'message': message,
                }
            )
        
        # Evaluate using ChatGPT
        result = chatgpt_service.evaluate(
            question = request.form['question'],
            answer = request.form['answer'],
            confidence = request.form['confidence'],
        )

        # Send the result to backend
        if (request.headers.get('Authorization', '') != ''):
            # Define the headers
            headers = {
                'Authorization': request.headers['Authorization'],
            }

            # Define the data
            data = {
                'finished': 1,
                'fluency_feedback': result.fluency.json(),
                'pronunciation_feedback': result.pronunciation.json(),
                'grammar_feedback': result.grammar.json(),
                'lexical_feedback': result.lexical.json(),
            }

            # Send the request to the Englishvit API
            response = requests.post(
                f"https://englishvit.com/api/user/ielts-ai/test/update/{request.form['test_id']}", 
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