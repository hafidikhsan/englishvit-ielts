# MARK: Imports
# Modules.
from app.core.services.response import standart_response
from app.transcribe.models.exception import (
    TranscribeErrorException, 
    TranscribeClientException, 
    TranscribeServerException
)

# MARK: ErrorException
# Define an exception handler for TranscribeErrorException.
async def error_exception_handler(_, exc: TranscribeErrorException):
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

# MARK: ClientException
# Define an exception handler for TranscribeClientException.
async def client_exception_handler(_, exc: TranscribeClientException):
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

# MARK: ServerException
# Define an exception handler for TranscribeServerException.
async def server_exception_handler(_, exc: TranscribeServerException):
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