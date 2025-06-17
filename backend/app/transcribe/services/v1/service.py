# MARK: Import
# Dependencies.
from datetime import datetime
from fastapi import File, Form, Header, Request, UploadFile
import json
import logging
from openai import OpenAI
import os
from pydub import AudioSegment
import requests
from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from typing import Any, Optional

# Modules.
from app.core.services.response import standart_response
from app.transcribe.models.exception import TranscribeErrorException, TranscribeClientException, TranscribeServerException
from app.transcribe.models.response import TranscribeResponseModel
from config import EvIELTSConfig

# MARK: Variables
# Define some constants for transcribe services.
_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
_public_dir = os.path.join(_base_dir, "public")
_whisper_initial_prompt = "I was like, was like, I'm like, you know what I mean, kind of, um, ah, huh, and so, so um, uh, and um, like um, so like, like it's, it's like, i mean, yeah, ok so, uh so, so uh, yeah so, you know, it's uh, uh and, and uh, like, kind"
_use_silero_vad = True

# MARK: PrivateFunctions
# Function to convert an audio to wav format.
def _convert_audio_to_wav(audio_file_path: str) -> str:
    """
    Convert an audio file to WAV format.

    Args:
        audio_file_path (str): The path to the audio file to be converted.

    Returns:
        str: The path to the converted WAV file.
    """
    try:
        # Check if the audio file exists.
        if not os.path.exists(audio_file_path):
            # Log the error for debugging purposes.
            logging.error(f"Audio file not found: {audio_file_path}")

            # Raise an exception if the audio file does not exist.
            raise TranscribeErrorException(
                information="Audio Conversion",
                detail=f"Audio file not found: {audio_file_path}"
            )
        
        # Get the original file extension.
        file_extension = os.path.splitext(audio_file_path)[1][1:].lower()

        # Get original file name without extension.
        file_name = os.path.splitext(os.path.basename(audio_file_path))[0]

        # Load the audio file using pydub.
        audio = AudioSegment.from_file(audio_file_path, format=file_extension)

        # Resample the audio to 16kHz and convert to mono.
        audio = audio.set_frame_rate(16000).set_channels(1)

        # Get the original directory to save the converted file.
        original_directory = os.path.dirname(audio_file_path)

        # Define the output WAV file path.
        wav_file_path = os.path.join(original_directory, f"{file_name}_clean.wav")

        # Export the audio to WAV format.
        audio.export(wav_file_path, format="wav")

        # Check if the WAV file wasn't created successfully.
        if not os.path.exists(wav_file_path):
            # Log the error for debugging purposes.
            logging.error(f"Conversion audio not found: {audio_file_path}")

            # Raise an exception if the conversion fails.
            raise TranscribeErrorException(
                information="Audio Conversion",
                detail=f"Conversion audio not found: {audio_file_path}"
            )
        
        # Return the path to the converted WAV file.
        return wav_file_path
    
    except TranscribeErrorException as error:
        # Re-raise the TranscribeErrorException for further handling.
        raise error
    
    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Unexpected error during audio conversion: {str(error)}")

        # Raise a TranscribeErrorException for any unexpected errors.
        raise TranscribeErrorException(
            information="Audio Conversion",
            detail=str(error)
        )
    
# Function to delete the audio file.
def _delete_audio_file(audio_file_path: str) -> None:
    """
    Delete the specified audio file.

    Args:
        audio_file_path (str): The path to the audio file to be deleted.
    """
    try:
        # Check if the audio file exists.
        if os.path.exists(audio_file_path):
            # Remove the audio file.
            os.remove(audio_file_path)

        else:
            # Log the error if the audio file does not exist.
            logging.error(f"Audio file not found for deletion: {audio_file_path}")

            # Raise an exception if the audio file does not exist.
            raise TranscribeErrorException(
                information="Audio Deletion",
                detail=f"Audio file not found for deletion: {audio_file_path}"
            )
        
    except TranscribeErrorException as error:
        # Re-raise the TranscribeErrorException for further handling.
        raise error
    
    except Exception as error:
        # Log any errors that occur during deletion.
        logging.error(f"Error deleting audio file: {str(error)}")

        # Raise a TranscribeErrorException for any unexpected errors.
        raise TranscribeErrorException(
            information="Audio Deletion",
            detail=str(error)
        )
    
# MARK: LoadSileroVADModel
# Function to load the Silero VAD model.
def load_silero_vad_model():
    """
    Load the Silero Voice Activity Detection (VAD) model.

    Returns:
        model: The loaded Silero VAD model.
    """
    try:
        # Log the loading of the Silero VAD model.
        logging.info("Loading Silero VAD model...")

        # Load the Silero VAD model.
        model = load_silero_vad()

        # Log the successful loading of the model.
        logging.info("Silero VAD model loaded successfully.")

        # Check if the model is loaded correctly.
        if model is None:
            # Log the error for debugging purposes.
            logging.error("Failed to load Silero VAD model")

            # Raise an exception if the model loading fails.
            raise TranscribeErrorException(
                information="Silero VAD Model Loading",
                detail="Failed to load Silero VAD model"
            )
        
        # Return the loaded model.
        return model
    
    except TranscribeErrorException as error:
        # Re-raise the TranscribeErrorException for further handling.
        raise error
    
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error loading Silero VAD model: {str(error)}")

        # Raise an exception if the model loading fails.
        raise TranscribeErrorException(
            information="Silero VAD Model Loading",
            detail=str(error)
        )

# MARK: Transcribe
# Transcribe service to handle transcription requests.
async def transcribe(
    request: Request,
    file: Optional[UploadFile] = File(None),
    authorization: Optional[str] = Header(None),
    test_id: Optional[Any] = Form(None)
) -> dict:
    """
    Service to handle audio file transcription requests.

    Args:
        request (Request): The request object for get the model.
        file (Optional[UploadFile]): The audio file to be transcribed.
        authorization (Optional[str]): The authorization header for the request.
        test_id (Optional[str]): An optional test identifier for tracking.

    Returns:
        dict: A dictionary containing the transcription result and word timestamps.
    """
    # Define the audio file path.
    audio_file_path = None

    # Check if the file is provided.
    if file is None:
        # Log the error for debugging purposes.
        logging.error("No audio file provided for transcription")

        # Raise an exception if no audio file is provided.
        raise TranscribeClientException(
            information="GET -> Transcribe",
            detail="Audio file is required"
        )

    try:
        # Define allowed file extensions for audio files.
        allowed_extensions = ["mp3", "wav", "m4a"]

        # Get the file data.
        file_data = await file.read()

        # Check if the file has a valid extension.
        if not file.filename.split(".")[-1].lower() in allowed_extensions:
            # Log the error for debugging purposes.
            logging.error(f"Invalid file type: {file.filename}")

            # Raise an exception if the file type is not supported.
            raise TranscribeClientException(
                information="GET -> Transcribe",
                detail="Unsupported file type. Allowed types: mp3, wav, m4a"
            )
        
        # Check if audio folder in public directory exists, if not create it.
        audio_folder = os.path.join(_public_dir, "audio")
        os.makedirs(audio_folder, exist_ok=True)

        # Split the file name and extension.
        _, file_extension = os.path.splitext(file.filename)

        # Define the file name without extension.
        file_name = f"_{datetime.now().isoformat()}"

        # Get the authorization header value.
        if authorization:
            # Use the authorization header value and test ID as the file name.
            file_name = authorization.split(" ")[-1] + str("_" + test_id if test_id is not None else "") + file_name
        else:
            # If no authorization header is provided, use a default file name.
            file_name = "transcription" + file_name

        # Define the path to save the audio file.
        audio_file_path = os.path.join(audio_folder, file_name + file_extension)

        # Save the audio file to the specified path.
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(file_data)

        # Get the converted WAV file path.
        converted_audio_path = _convert_audio_to_wav(audio_file_path)

        # Delete the original audio file after conversion.
        _delete_audio_file(audio_file_path)

        # Change the audio file path to the converted WAV file path.
        audio_file_path = converted_audio_path

        # Variable to hold a flag of the VAD model usage.
        speech_timestamps = []

        # If Silero VAD is enabled, load the model.
        if _use_silero_vad:
            # Get the Silero VAD model from the request state.
            vad_model = request.app.state.vad_model

            # Read the audio file using Silero VAD.
            wav_vad = read_audio(audio_file_path)

            # Get speech timestamps from the audio file.
            speech_timestamps = get_speech_timestamps(
                wav_vad, 
                vad_model, 
                return_seconds=True
            )

        else:
            # If Silero VAD is not enabled, add dummy variable to hold speech timestamps.
            speech_timestamps = [1]

        # Define the response model for transcription.
        response_model: TranscribeResponseModel = None
        
        # Check if not have speech timestamps.
        if not speech_timestamps:
            # Set the response model with an empty transcription.
            response_model = TranscribeResponseModel(
                transcribe="",
                word_timestamp=json.dumps([])
            )

        else:
            # Define the OpenAI Whisper client.
            openai_client = OpenAI(
                api_key=EvIELTSConfig.openai_api_key
            )

            # Open the audio file for transcription.
            audio_file = open(audio_file_path, "rb")

            # Transcribe the audio file using OpenAI Whisper.
            transcription = openai_client.audio.transcriptions.create(
                file=audio_file,
                model=EvIELTSConfig.openai_whisper_model_name,
                language="en",
                prompt=_whisper_initial_prompt,
                response_format="verbose_json",
                temperature=0.0,
                timestamp_granularities=["word"],
            )

            # Get the transcribed text from the response.
            transcribed_text = transcription.text

            # Get the word timestamps from the transcription.
            word_timestamps = []
            for word in transcription.words:
                # Append the word and its start and end timestamps to the list.
                word_timestamps.append({
                    "word": word.word,
                    "start": word.start,
                    "end": word.end
                })

            # Set the response model with the transcribed text and word timestamps.
            response_model = TranscribeResponseModel(
                transcribe=transcribed_text,
                word_timestamp=json.dumps(word_timestamps)
            )

        # Check if the authorization header is provided.
        if authorization:
            # Check if the test ID is not provided.
            if test_id is None:
                # Log the error for debugging purposes.
                logging.error("Test ID is missing")

                # Raise an exception if the test ID is not provided.
                raise TranscribeClientException(
                    information="GET -> Transcribe",
                    detail="Test ID is required when authorization is provided"
                )
            
            # Open the audio file for reading.
            with open(audio_file_path, "rb") as audio_file:
                # Read the audio file data.
                audio_data = audio_file.read()

                # Define headers for the request.
                headers = {
                    "Authorization": authorization,
                }

                # Define the body for the request.
                body = {
                    "transcribe": response_model.transcribe,
                    "words_timestamp": response_model.word_timestamp,
                    "audio": audio_data,
                }

                # Request the transcription service to save the transcription.
                response = requests.post(
                    f"https://englishvit.com/api/user/ielts-ai/test/update/{test_id}", 
                    data = body, 
                    headers = headers
                )

                # Check if the response is not successful
                if response.status_code != 200:
                    # Log the error for debugging purposes.
                    logging.error(f"Failed to save transcription for test id: {test_id}")

                    # Raise an exception if the transcription saving fails.
                    raise TranscribeServerException(
                        information="Transcription Saving",
                        detail=f"Failed to save transcription for test id: {test_id}"
                    )
                
        # Delete the audio file after saving the transcription.
        _delete_audio_file(audio_file_path)

        # Set audio file path to None to avoid deletion again.
        audio_file_path = None

        # Return the response model as a dictionary.
        return response_model.dict()
        
    except TranscribeErrorException as error:
        # Check if the audio file path is provided and delete it.
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Log the error for debugging purposes.
        logging.error(f"Transcription error: {error.detail}")

        # Re-raise the TranscribeErrorException for further handling.
        raise error
    
    except TranscribeClientException as error:
        # Check if the audio file path is provided and delete it.
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Log the client exception for debugging purposes.
        logging.error(f"Client error: {error.detail}")

        # Re-raise the TranscribeClientException for further handling.
        raise error

    except TranscribeServerException as error:
        # Check if the audio file path is provided and delete it.
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Log the server exception for debugging purposes.
        logging.error(f"Server error: {error.detail}")

        # Re-raise the TranscribeServerException for further handling.
        raise error
    
    except Exception as error:
        # Check if the audio file path is provided and delete it.
        if audio_file_path:
            _delete_audio_file(audio_file_path)

        # Log the unexpected error for debugging purposes.
        logging.error(f"Unexpected error: {error}")

        # Raise a TranscribeErrorException for any unexpected errors.
        raise TranscribeErrorException(
            information="Unexpected error occurred",
            detail=str(error)
        )
    
# MARK: GetTranscribeServiceInfo
# Function to get the transcribe service information.
async def get_transcribe_service_info() -> dict:
    """
    Get the transcribe service information.

    Returns:
        dict: A dictionary containing the transcribe service information.
    """
    # Return a success response with the transcribe service information.
    return {
        "initial_prompt": _whisper_initial_prompt,
        "whisper_model_name": EvIELTSConfig.openai_whisper_model_name,
        "use_silero_vad": _use_silero_vad,
    }
    
# MARK: UpdateWhisperModelName
# Function to update the Whisper model name in the configuration.
async def update_whisper_model_name(
    model_name: Optional[str] = Form(None)
) -> dict:
    """
    Update the Whisper model name in the configuration.

    Args:
        model_name (str): The new Whisper model name to be set.

    Returns:
        dict: A dictionary containing the updated Whisper model name.
    """
    # Check if the model name is provided.
    if not model_name:
        # Log the error for debugging purposes.
        logging.error("Model name is required for updating Whisper model")

        # Raise an exception if the model name is not provided.
        raise TranscribeClientException(
            information="GET -> Update Whisper Model Name",
            detail="Model name is required"
        )
    
    # Update the Whisper model name in the configuration.
    EvIELTSConfig.openai_whisper_model_name = model_name

    # Return a success response with the updated model name.
    return {
        "model_name": EvIELTSConfig.openai_whisper_model_name
    }

# MARK: UpdateWhisperInitialPrompt
# Function to update the Whisper initial prompt in the configuration.
async def update_whisper_initial_prompt(
    initial_prompt: Optional[str] = Form(None)
) -> dict:
    """
    Update the Whisper initial prompt in the configuration.

    Args:
        initial_prompt (str): The new Whisper initial prompt to be set.

    Returns:
        dict: A dictionary containing the updated Whisper initial prompt.
    """
    # Check if the initial prompt is provided.
    if not initial_prompt:
        # Log the error for debugging purposes.
        logging.error("Initial prompt is required for updating Whisper initial prompt")

        # Raise an exception if the initial prompt is not provided.
        raise TranscribeClientException(
            information="GET -> Update Whisper Initial Prompt",
            detail="Initial prompt is required"
        )
    
    # Update the Whisper initial prompt in the configuration.
    global _whisper_initial_prompt
    _whisper_initial_prompt = initial_prompt

    # Return a success response with the updated initial prompt.
    return {
        "initial_prompt": _whisper_initial_prompt
    }

# MARK: UpdateUseSileroVAD
# Function to update the Silero VAD usage in the configuration.
async def update_use_silero_vad(
    use_silero_vad: Optional[str] = Form(None)
) -> dict:
    """
    Update the Silero VAD usage in the configuration.

    Args:
        use_silero_vad (bool): A flag indicating whether to use Silero VAD.

    Returns:
        dict: A dictionary containing the updated Silero VAD usage status.
    """
    # Check if the use_silero_vad is provided.
    if use_silero_vad is None:
        # Log the error for debugging purposes.
        logging.error("Use Silero VAD flag is required for updating Silero VAD usage")

        # Raise an exception if the use_silero_vad is not provided.
        raise TranscribeClientException(
            information="GET -> Update Use Silero VAD",
            detail="Use Silero VAD flag is required"
        )
    
    try:
        # Parse the use_silero_vad value to a boolean.
        int_use_silero_vad = int(use_silero_vad)

        # Check if the parsed value is not 0 or 1.
        if int_use_silero_vad not in [0, 1]:
            # Log the error for debugging purposes.
            logging.error("Invalid value for use_silero_vad. Must be 0 or 1")

            # Raise an exception if the value is not valid.
            raise TranscribeClientException(
                information="GET -> Update Use Silero VAD",
                detail="Use Silero VAD must be 0 or 1"
            )
        
        # Convert the integer value to a boolean.
        target_value = bool(int_use_silero_vad)

        # Update the Silero VAD usage in the configuration.
        global _use_silero_vad
        _use_silero_vad = target_value

        # Return a success response with the updated Silero VAD usage status.
        return {
            "use_silero_vad": _use_silero_vad
        }

    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error updating use_silero_vad: {str(error)}")

        # Raise a TranscribeClientException for any unexpected errors.
        raise TranscribeClientException(
            information="GET -> Update Use Silero VAD",
            detail=str(error)
        )

# MARK: ExceptionHandler
# Define an exception handler for TranscribeErrorException.
async def transcribe_error_exception_handler(_, exc: TranscribeErrorException):
    """
    Exception handler for TranscribeErrorException.

    Args:
        _: The request object.
        exc: The TranscribeErrorException instance.

    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Error",
        message=f"An error occurred while processing the transcribe"
    )

# Define an exception handler for TranscribeClientException.
async def transcribe_client_exception_handler(_, exc: TranscribeClientException):
    """
    Exception handler for TranscribeClientException.

    Args:
        _: The request object.
        exc: The TranscribeClientException instance.

    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Client Error",
        message=f"A client error occurred while processing the transcribe"
    )

# Define an exception handler for TranscribeServerException.
async def transcribe_server_exception_handler(_, exc: TranscribeServerException):
    """
    Exception handler for TranscribeServerException.

    Args:
        _: The request object.
        exc: The TranscribeServerException instance.
    
    Returns:
        dict: A standardized error response.
    """

    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Server Error",
        message=f"A server error occurred while processing the transcribe"
    )