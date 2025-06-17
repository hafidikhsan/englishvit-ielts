# MARK: Import
# Dependencies.
from fastapi import APIRouter, File, Form, Header, Request, UploadFile
from typing import Any, Optional

# Modules.
from app.core.models.response import ResponseModel
from app.core.services.response import standart_response
from app.transcribe.services.v1 import service

# MARK: Router
# Create a new APIRouter instance for the transcribe routes.
router = APIRouter(
    prefix="/api/v1/transcribe",
    tags=["Transcribe Routes Version 1"],
)

# MARK: Variables
# Define some constants for the API routes.
_audio = "/audio"
_info = "/info"
_settings = "/settings"

# MARK: Transcribe
# Define a transcribe route for the API to transcribe audio files.
@router.post(_audio, response_model=ResponseModel)
async def transcribe_audio(
    request: Request,
    file: Optional[UploadFile] = File(None),
    authorization: Optional[str] = Header(None),
    test_id: Optional[Any] = Form(None)
) -> ResponseModel:
    """
    Transcribe audio file.

    Args:
        request (Request): The HTTP request object.
        file (Optional[UploadFile]): The audio file to be transcribed.
        authorization (Optional[str]): The authorization header for the request.
        test_id (Optional[Any]): An optional test identifier for tracking.

    Returns:
        ResponseModel: The response model containing the transcription result.
    """
    # Call the transcribe service to process the audio file.
    result = await service.transcribe(
        request=request,
        file=file,
        authorization=authorization,
        test_id=test_id
    )

    # Return the standardized response.
    return standart_response(
        data=result,
        code=200,
        status="Success",
        message="Audio transcription completed successfully."
    )

# Define a route to get information about the transcribe service.
@router.get(_info, response_model=ResponseModel)
async def get_transcribe_info() -> ResponseModel:
    """
    Get information about the transcribe service.

    Returns:
        ResponseModel: The response model containing service information.
    """
    # Fetch transcribe service information.
    info = await service.get_transcribe_service_info()

    # Return the standardized response.
    return standart_response(
        data=info,
        code=200,
        status="Success",
        message="Transcribe service information retrieved successfully."
    )

# Define a route to update the whisper model name.
@router.post(_settings + "/whisper", response_model=ResponseModel)
async def update_whisper_model_name(
    model_name: Optional[Any] = Form(None)
) -> ResponseModel:
    """
    Update the Whisper model name.

    Args:
        model_name (Optional[Any]): The name of the Whisper model to be set.

    Returns:
        ResponseModel: The response model containing whisper model settings.
    """
    # Fetch whisper model settings.
    settings = await service.update_whisper_model_name(
        model_name=model_name
    )

    # Return the standardized response.
    return standart_response(
        data=settings,
        code=200,
        status="Success",
        message="Whisper model name updated successfully."
    )

# Define a route to update the initial prompt for the transcription service.
@router.post(_settings + "/initial-prompt", response_model=ResponseModel)
async def update_whisper_initial_prompt(
    initial_prompt: Optional[Any] = Form(None)
) -> ResponseModel:
    """
    Update the initial prompt for the transcription service.

    Args:
        initial_prompt (Optional[Any]): The new initial prompt to be set.

    Returns:
        ResponseModel: The response model containing updated initial prompt settings.
    """
    # Fetch updated initial prompt settings.
    settings = await service.update_whisper_initial_prompt(
        initial_prompt=initial_prompt
    )

    # Return the standardized response.
    return standart_response(
        data=settings,
        code=200,
        status="Success",
        message="Whisper initial prompt updated successfully."
    )

# Define a route to update the use silero VAD.
@router.post(_settings + "/use-silero-vad", response_model=ResponseModel)
async def update_use_silero_vad(
    use_silero_vad: Optional[Any] = Form(None)
) -> ResponseModel:
    """
    Update the use of Silero VAD.

    Args:
        use_silero_vad (Optional[Any]): Flag to enable or disable Silero VAD.

    Returns:
        ResponseModel: The response model containing updated Silero VAD settings.
    """
    # Fetch updated Silero VAD settings.
    settings = await service.update_use_silero_vad(
        use_silero_vad=use_silero_vad
    )

    # Return the standardized response.
    return standart_response(
        data=settings,
        code=200,
        status="Success",
        message="Silero VAD settings updated successfully."
    )