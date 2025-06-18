# MARK: Import
# Dependencies.
from fastapi import HTTPException

# MARK: TranscribeException
# Base class for transcribe-related exceptions inheriting from HTTPException. This class is used to
# provide a consistent structure for transcribe-related errors in the application.
class TranscribeException(HTTPException):
    """
    Base class for transcribe-related exceptions.
    Inherits from HTTPException to provide HTTP status codes and messages.
    This class can be extended to create specific transcribe-related exceptions.
    """
    pass

# MARK: ErrorException
# Exception raised for errors related to transcribe retrieval or processing.
class TranscribeErrorException(TranscribeException):
    """
    Exception raised for general transcribe-related errors.
    Inherits from TranscribeException to provide a 500 Internal Server Error status code.

    General error in server processing of transcribe-related operations.
    """
    def __init__(self, information: str, detail: str):
        # Define the error details.
        error_details = {
            "information": information,
            "detail": detail
        }

        # Call the parent constructor with a 500 status code and the message.
        super().__init__(status_code=500, detail=error_details)

# MARK: ClientException
# Exception raised for client-related errors in transcribe retrieval or processing.
class TranscribeClientException(TranscribeException):
    """
    Exception raised for client-related errors in transcribe retrieval or processing.
    Inherits from TranscribeException to provide a 400 Bad Request status code.

    Client error in transcribe retrieval or processing, such as invalid input or request.
    """
    def __init__(self, information: str, detail: str):
        # Define the error details.
        error_details = {
            "information": information,
            "detail": detail
        }

        # Call the parent constructor with a 400 status code and the message.
        super().__init__(status_code=400, detail=error_details)

# MARK: ServerException
# Exception raised for server-related errors in transcribe retrieval or processing.
class TranscribeServerException(TranscribeException):
    """
    Exception raised for server-related errors in transcribe retrieval or processing.
    Inherits from TranscribeException to provide a 503 Service Unavailable status code.

    Server origin error in transcribe retrieval or processing, such as database issues or
    service unavailability for origin services.
    """
    def __init__(self, information: str, detail: str):
        # Define the error details.
        error_details = {
            "information": information,
            "detail": detail
        }

        # Call the parent constructor with a 503 status code and the message.
        super().__init__(status_code=503, detail=error_details)