# MARK: Import
# Dependencies
import os
from flask import jsonify, request, current_app

# Routes
from app.api.routes import api_bp, api_v2_bp

# Services
from app.services.chat_gpt_service import chatgpt_service
from app.services.asr_service import asr_service
from app.services.ielts_services import ielts_service

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvClientException, EvServerException, EvException
from app.models.response_model import EvResponseModel
from app.models.response_metadata_model import EvResponseMetadataModel

# Get the JSON directory
def get_json_dir():
    return os.path.abspath(os.path.join(current_app.root_path, "..", "json_data"))

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
    
# MARK: Settings
@api_v2_bp.route('/settings/<type>', methods = ['POST'])
def settings(type: str):
    '''
    Function to handle the settings for the services.
    '''
    try:
        # Check if type is setting model
        if type == 'model':
            # Get the model name from the request
            chatgpt_feedback_model_name = request.form.get('chatgpt_feedback_model_name', None)
            chatgpt_whisper_model_name = request.form.get('chatgpt_whisper_model_name', None)

            # Update the IELTS model
            ielts_service.update_model(
                chatgpt_feedback_model_name = chatgpt_feedback_model_name,
                chatgpt_whisper_model_name = chatgpt_whisper_model_name,
            )

            # Define the response model data
            response_data = EvResponseModel(
                metadata = EvResponseMetadataModel(
                    code = 200,
                    status = 'Success',
                    message = 'IELTS model updated successfully',
                ),
                data = {
                    'chatgpt_feedback_model_name': chatgpt_feedback_model_name,
                    'chatgpt_whisper_model_name': chatgpt_whisper_model_name,
                }
            )

            # Return the settings response
            return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
        
        # Check if type is setting asr initial prompt
        elif type == 'initial-prompt':
            # Check if the request has a text `initial_prompt` field
            if 'initial_prompt' not in request.form:
                # Define the error message
                message = 'Invalid request initial_prompt are required'

                # Throw an exception
                raise EvClientException(
                    message = message,
                )
            
            # Get the model name from the request
            initial_prompt = request.form['initial_prompt'],

            # Update the initial prompt
            ielts_service.update_initial_prompt(initial_prompt = initial_prompt)

            # Define the response model data
            response_data = EvResponseModel(
                metadata = EvResponseMetadataModel(
                    code = 200,
                    status = 'Success',
                    message = 'Initial prompt updated successfully',
                ),
                data = {
                    'initial_prompt': initial_prompt,
                }
            )

            # Return the settings response
            return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
        
        # Check if type is setting evaluation prompt
        elif type == 'evaluation-prompt':
            try:
                json_dir = get_json_dir()
                file_path = os.path.join(json_dir, EvIELTSConfig.evaluation_feedback_prompt)

                # Check if the request has files and if the file is present
                if not request.files or 'file' not in request.files:
                    # Define the error message
                    message = 'Invalid request, text file is required'

                    # Throw an exception
                    raise EvClientException(
                        message = message,
                    )
                
                # Define list of allowed text file extensions
                allowed_extensions = ['txt']

                # Get the text file from the request
                text_file = request.files['file']

                # Check if the file is allowed
                if text_file.filename.split('.')[-1].lower() not in allowed_extensions:
                    # Define the error message
                    message = 'Invalid file type. Allowed types are: text files (.txt)'

                    # Throw an exception
                    raise EvClientException(
                        message = message,
                    )
                
                # Read the content of the text file
                text_content = text_file.read().decode('utf-8')

                # Write the new data to the file
                with open(file_path, 'w') as f:
                    # Replace the content of the file with the new text content
                    f.write(text_content)

                # Update the evaluation feedback prompt
                ielts_service.update_prompt()

                # Define the response model data
                response_data = EvResponseModel(
                    metadata = EvResponseMetadataModel(
                        code = 200,
                        status = 'Success',
                        message = 'Information updated successfully',
                    ),
                    data = {
                        'information': text_content,
                    }
                )

                # Return the information response
                return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
                
            except Exception as e:
                # Error writing to file
                raise EvServerException(
                    message = "Error writing to file",
                )
            
        # Check if type is setting overall prompt
        elif type == 'overall-prompt':
            try:
                json_dir = get_json_dir()
                file_path = os.path.join(json_dir, EvIELTSConfig.overall_feedback_prompt)

                # Check if the request has files and if the file is present
                if not request.files or 'file' not in request.files:
                    # Define the error message
                    message = 'Invalid request, text file is required'

                    # Throw an exception
                    raise EvClientException(
                        message = message,
                    )
                
                # Define list of allowed text file extensions
                allowed_extensions = ['txt']

                # Get the text file from the request
                text_file = request.files['file']

                # Check if the file is allowed
                if text_file.filename.split('.')[-1].lower() not in allowed_extensions:
                    # Define the error message
                    message = 'Invalid file type. Allowed types are: text files (.txt)'

                    # Throw an exception
                    raise EvClientException(
                        message = message,
                    )
                
                # Read the content of the text file
                text_content = text_file.read().decode('utf-8')

                # Write the new data to the file
                with open(file_path, 'w') as f:
                    # Replace the content of the file with the new text content
                    f.write(text_content)

                # Update the evaluation feedback prompt
                ielts_service.update_prompt()

                # Define the response model data
                response_data = EvResponseModel(
                    metadata = EvResponseMetadataModel(
                        code = 200,
                        status = 'Success',
                        message = 'Information updated successfully',
                    ),
                    data = {
                        'information': text_content,
                    }
                )

                # Return the information response
                return jsonify(response_data.model_dump()), 200, {'ContentType' : 'application/json'}
                
            except Exception as e:
                # Error writing to file
                raise EvServerException(
                    message = "Error writing to file",
                )

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