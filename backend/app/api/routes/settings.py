# MARK: Import
# Dependencies
from flask import jsonify, request

# Routes
from app.api.routes import api_bp

# Services
from app.services.chat_gpt_service import chatgpt_service
from app.services.asr_service import asr_service

# Modules
from app.utils.exception import EvClientException, EvException
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel

# MARK: Settings
@api_bp.route('/settings/<type>', methods = ['POST'])
def settings(type: str):
    '''
    Function to handle the settings for the services.
    '''
    try:
        # Check if type is setting asr model
        if type == 'asr-model':
            # Check if the request has a text `model_name` field
            if 'model_name' not in request.form:
                # Define the error message
                message = 'Invalid request model_name are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the model name from the request
            model_name = request.form['model_name'],

            # Update the ASR model
            asr_service.update_model(model_name = model_name)

            # Define the response model data
            response_data = EvResponseModel(
                metadata = EvResponseMetadataModel(
                    code = 200,
                    status = 'Success',
                    message = 'ASR model updated successfully',
                ),
                data = {
                    'model': model_name,
                }
            )

            # Return the settings response
            return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
        
        # Check if type is setting asr initial prompt
        elif type == 'asr-initial-prompt':
            # Check if the request has a text `initial_prompt` field
            if 'initial_prompt' not in request.form:
                # Define the error message
                message = 'Invalid request initial_prompt are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the model name from the request
            initial_prompt = request.form['initial_prompt'],

            # Update the ASR initial prompt
            asr_service.update_initial_prompt(initial_prompt = initial_prompt)

            # Define the response model data
            response_data = EvResponseModel(
                metadata = EvResponseMetadataModel(
                    code = 200,
                    status = 'Success',
                    message = 'ASR initial prompt updated successfully',
                ),
                data = {
                    'initial_prompt': initial_prompt,
                }
            )

            # Return the settings response
            return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
        
        # Check if type is setting chat gpt model
        elif type == 'chatgpt-model':
            # Check if the request has a text `model_name` field
            if 'model_name' not in request.form:
                # Define the error message
                message = 'Invalid request model_name are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the model name from the request
            model_name = request.form['model_name'],

            # Update the ChatGPT model
            chatgpt_service.update_model(model_name = model_name)

            # Define the response model data
            response_data = EvResponseModel(
                metadata = EvResponseMetadataModel(
                    code = 200,
                    status = 'Success',
                    message = 'ChatGPT model updated successfully',
                ),
                data = {
                    'model': model_name,
                }
            )

            # Return the settings response
            return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
        
        # Check if type is setting chatgpt prompt
        elif type == 'chatgpt-prompt':
            # Get the model name from the request
            fluency_prompt = request.form.get('fluency_prompt', None)
            lexical_prompt = request.form.get('lexical_prompt', None)
            grammar_prompt = request.form.get('grammar_prompt', None)
            pronunciation_prompt = request.form.get('pronunciation_prompt', None)

            # Update the ChatGPT prompt
            chatgpt_service.update_prompt(
                fluency_prompt = fluency_prompt,
                lexical_prompt = lexical_prompt,
                grammar_prompt = grammar_prompt,
                pronunciation_prompt = pronunciation_prompt,
            )

            # Get the prompt from the ChatGPT service
            chatgpt_prompt = chatgpt_service.get_prompt()

            # Define the response model data
            response_data = EvResponseModel(
                metadata = EvResponseMetadataModel(
                    code = 200,
                    status = 'Success',
                    message = 'ChatGPT prompt updated successfully',
                ),
                data = chatgpt_prompt,
            )

            # Return the settings response
            return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}

        else:
            raise EvClientException(
                message = "Invalid type",
            )
    
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
                message = 'Internal server error in settings',
            ),
            data = {
                'message': 'Internal server error in settings',
                'information': str(error),
            }
        )

        # Return the error message
        return jsonify(response_data.model_dump()), 500, {'ContentType' : 'application/json'}