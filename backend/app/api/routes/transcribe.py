# MARK: Import
# Dependencies
import os
import requests
import json
from pydub import AudioSegment
from flask import jsonify, request

# Routes
from app.api.routes import api_bp

# Services
from app.services.asr_service import asr_service

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvServerException, EvClientException, EvAPIException
from app.models.response_model import EvResponseModel

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
                information = {
                    'message': message,
                }
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
                information = {
                    'message': message,
                }
            )
        
        # Return the output file path
        return output_path
    
    except EvServerException as error:
        # Re-raise the error
        raise error
    
    except Exception as error:
        # Define the error message
        message = f'Failed to convert audio to wav: {str(error)}'

        # Throw an exception
        raise EvServerException(
            message = message,
            information = {
                'message': message,
            }
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
                information = {
                    'message': message,
                }
            )
    
    except EvServerException as error:
        # Re-raise the error
        raise error
    
    except Exception as error:
        # Define the error message
        message = f'Failed to delete audio file: {str(error)}'

        # Throw an exception
        raise EvServerException(
            message = message,
            information = {
                'message': message,
            }
        )

# MARK: Transcribe
@api_bp.route('/transcribe', methods = ['POST'])
def transcribe():
    '''
    Function to transcribe the audio file. The function will take the audio file
    from the request, and some additional data from the request, and save the data 
    to the main server database. The function will then process the audio file to 
    get the transcribe text and word level time stamps. The function also convert 
    the audio file to wav format and resample the audio file to 16kHz and convert 
    it to mono. The function will then return the transcribe text, word level time 
    stamps and some additional data from the request. The function will also delete 
    the original audio file in server after processing.

    Important: The function also contain a request to the Englishvit API to
    send the transcribe text, word level time stamps, resampled audio file and
    some additional data from the request to the main server database.
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
                information = {
                    'message': message,
                }
            )
        
        # Check if the request has a text `test_id` field
        if 'test_id' not in request.form:
            # Define the error message
            message = 'Invalid request, test_id is required'

            # Throw an exception
            raise EvClientException(
                message = message,
                information = {
                    'message': message,
                }
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
                information = {
                    'message': message,
                }
            )
        
        # Check if the file size is greater than 50MB
        if audio_file.content_length > 50 * 1024 * 1024:
            # Define the error message
            message = 'File size exceeds the limit of 50MB'

            # Throw an exception
            raise EvClientException(
                message = message,
                information = {
                    'message': message,
                }
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

        # Transcribe the audio file
        (transcribe, words) = asr_service.process_audio(audio_file_path)

        # Send the result to backend
        if (request.headers.get('Authorization', '') != ''):
            # Load the audio file
            with open(audio_file_path, 'rb') as audio_file:
                # Read the audio file content
                audio_content = audio_file.read()

                # Define the headers
                headers = {
                    'Authorization': request.headers['Authorization']
                }

                # Define the data
                data = {
                    'transcribe': transcribe,
                    'words': json.dumps(words),
                    'audio': audio_content,  # Add audio content as BLOB
                }

                # Send the request to the Englishvit API
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/test/update/{request.form['test_id']}", 
                    data = data, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Define the error message
                    message = f'Failed to send the audio file to the server: {response.text}'

                    # Throw an exception
                    raise EvAPIException(
                        message = message,
                        information = {
                            'message': message,
                        }
                    )

        # Delete the audio file
        _delete_audio_file(audio_file_path)

        # Set audio file saved flag
        audio_file_path = None

        # Return the data
        return jsonify(EvResponseModel(
            code = 200,
            status = 'Success',
            message = 'Transcribe successful',
            data = {
                'transcribe': transcribe,
                'words': words,
                'test_id': request.form['test_id'],
            },
        ).to_dict()), 200, {'ContentType' : 'application/json'}
        
    except EvClientException as error:
        # Check if the audio file is saved and delete it
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Return the error message
        return jsonify(EvResponseModel(
            code = error.status_code,
            status = 'Error',
            message = error.message,
            data = {
                'error': {
                    'message': error.message,
                    'information': error.information,
                },
            },
        ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
    
    except EvServerException as error:
        # Check if the audio file is saved and delete it
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Return the error message
        return jsonify(EvResponseModel(
            code = error.status_code,
            status = 'Error',
            message = error.message,
            data = {
                'error': {
                    'message': error.message,
                    'information': error.information,
                },
            },
        ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
    
    except EvAPIException as error:
        # Check if the audio file is saved and delete it
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Return the error message
        return jsonify(EvResponseModel(
            code = error.status_code,
            status = 'Error',
            message = error.message,
            data = {
                'error': {
                    'message': error.message,
                    'information': error.information,
                },
            },
        ).to_dict()), error.status_code, {'ContentType' : 'application/json'}
    
    except Exception as error:
        # Check if the audio file is saved and delete it
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Return the error message
        return jsonify(EvResponseModel(
            code = 500,
            status = 'Error',
            message = 'Internal server error',
            data = {
                'error': {
                    'message': str(error),
                },
            },
        ).to_dict()), 500, {'ContentType' : 'application/json'}