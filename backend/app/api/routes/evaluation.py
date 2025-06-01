# MARK: Import
# Dependencies
import os
import requests
from pydub import AudioSegment
from flask import jsonify, request

# Routes
from app.api.routes import api_bp, api_v2_bp

# Services
from app.services.chat_gpt_service import chatgpt_service
from app.services.ielts_services import ielts_service

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvClientException, EvAPIException, EvServerException, EvException
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

# MARK: ConvertAudioToWav
def _convert_audio_to_wav(original_path: str) -> str:
    '''
    Custom function to convert audio to wav. Build using `pydub` to convert audio files
    to wav format. 

    Important: This function will only convert the audio file to wav format. It will not 
    delete the original file. The original file will be kept in the same directory as the
    converted file. The converted file will be saved in the same directory as the original
    file with the same name as the original file but with `_clean` suffix and `.wav` extension.
    The function will also resample the audio to 16kHz and convert it to mono.

    Args:
    - original_path: str: Path to the original audio file.

    Returns:
    - str: Path to the converted audio file.
    '''
    try:
        # Check if the original file exists
        if not os.path.exists(original_path):
            # Define the error message
            message = f'File not found while convert the audio to wav: {original_path}'

            # Throw an exception
            raise EvServerException(
                message = message,
            )
        
        # Get the original file extension
        original_file_ext = os.path.splitext(original_path)[1][1:].lower()

        # Get the original file name
        original_file_name = os.path.splitext(os.path.basename(original_path))[0]

        # Load the audio file using pydub
        audio = AudioSegment.from_file(
            original_path, 
            format = original_file_ext,
        )

        # Resample the audio to 16kHz and convert to mono
        audio = audio.set_frame_rate(EvIELTSConfig.audio_clean_sample_rate).set_channels(EvIELTSConfig.audio_clean_channels)

        # Get the directory of the original file
        original_directory = os.path.dirname(original_path)

        # Define the output file path
        output_path = os.path.join(
            original_directory, 
            f'{original_file_name}_clean.{EvIELTSConfig.audio_clean_extension}'
        )

        # Export the audio file as wav
        audio.export(
            output_path, 
            format = EvIELTSConfig.audio_clean_extension
        )

        # Check if the output file exists
        if not os.path.exists(output_path):
            # Define the error message
            message = f'Failed to convert audio to wav output not found: {output_path}'

            # Throw an exception
            raise EvServerException(
                message = message,
            )
        
        # Return the output file path
        return output_path
    
    except EvException as error:
        # Re-raise the error
        raise error
    
    except Exception as error:
        # Define the error message
        message = f'Failed to convert audio to wav: {str(error)}'

        # Throw an exception
        raise EvServerException(
            message = message,
        )
    
# MARK: DeleteAudioFile
def _delete_audio_file(file_path: str) -> None:
    '''
    Custom function to delete the audio file. The function will take the audio file
    path and delete the file from the server. The function will also check if the
    file exists before deleting it.

    Args:
    - file_path: str: Path to the audio file.
    '''
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
        else:
            # Define the error message
            message = f'File not found while deleting audio file: {file_path}'

            # Throw an exception
            raise EvServerException(
                message = message,
            )
    
    except EvException as error:
        # Re-raise the error
        raise error
    
    except Exception as error:
        # Define the error message
        message = f'Failed to delete audio file: {str(error)}'

        # Throw an exception
        raise EvServerException(
            message = message,
        )
        
# MARK: Evaluation
@api_v2_bp.route('/evaluation', methods = ['POST'])
def evaluation_v2():
    '''
    Function to handle the evaluation process.
    '''
    # A flag to check if the audio file is already saved
    audio_file_path = None

    try:
        # Check if the request has files and if the file is present
        if not request.files or 'file' not in request.files:
            # Define the error message
            message = 'Invalid request, audio file is required'

            # Throw an exception
            raise EvClientException(
                message = message,
            )
        
        # Check if the request has a text `question` and `test_id` field
        if 'test_id' not in request.form or 'question' not in request.form:
            # Define the error message
            message = 'Invalid request test_id and question is required'

            # Throw an exception
            raise EvClientException(
                message = message,
            )
        
        # Define list of allowed audio file extensions
        allowed_extensions = ['wav', 'mp3', 'm4a']

        # Get the audio file from the request
        audio_file = request.files['file']

        # Check if the file is allowed
        if audio_file.filename.split('.')[-1].lower() not in allowed_extensions:
            # Define the error message
            message = 'Invalid file type. Allowed types are: wav, mp3, m4a'

            # Throw an exception
            raise EvClientException(
                message = message,
            )
        
        # Check if the file size is greater than 50MB
        if audio_file.content_length > 50 * 1024 * 1024:
            # Define the error message
            message = 'File size exceeds the limit of 50MB'

            # Throw an exception
            raise EvClientException(
                message = message,
            )
        
        # Get the file name and extension
        file_name, file_extension = os.path.splitext(audio_file.filename)

        # Define main directory
        main_directory = '/app/audio'

        # Get the audio file path
        audio_file_path = os.path.join(main_directory, file_name + file_extension)

        # Save the audio file to the server
        audio_file.save(audio_file_path)

        # Convert the audio file to wav format and get the output path
        output_path = _convert_audio_to_wav(audio_file_path)

        # Delete the original audio file
        _delete_audio_file(audio_file_path)

        # Change the audio file path to the output path
        audio_file_path = output_path

        # Evaluate using ChatGPT
        result = ielts_service.evaluate(
            audio_file_path = audio_file_path,
            question = request.form['question'],
        )

        # Send the result to backend
        if (request.headers.get('Authorization', '') != ''):
            # Load the audio file
            with open(audio_file_path, 'rb') as audio_file:
                # Read the audio file content
                audio_content = audio_file.read()
                
                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization'],
                }

                # Define the data
                data = {
                    'finished': 1,
                    'transcribe': result.transcript,
                    'words_timestamp': result.word_timestamp,
                    'audio': audio_content, 
                    'fluency_feedback': result.evaluation.fluency.json(),
                    'pronunciation_feedback': result.evaluation.pronunciation.json(),
                    'grammar_feedback': result.evaluation.grammar.json(),
                    'lexical_feedback': result.evaluation.lexical.json(),
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
                    )
            
        # Delete the audio file
        _delete_audio_file(audio_file_path)

        # Set audio file saved flag
        audio_file_path = None

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
        # Check if the audio file is saved and delete it
        if audio_file_path:
            _delete_audio_file(audio_file_path)

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
        # Check if the audio file is saved and delete it
        if audio_file_path:
            _delete_audio_file(audio_file_path)

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