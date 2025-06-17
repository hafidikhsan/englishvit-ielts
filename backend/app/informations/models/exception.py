# MARK: Import
# Dependencies.
from fastapi import HTTPException

# MARK: InformationException
# Base class for information-related exceptions inheriting from HTTPException. This class is used to 
# provide a consistent structure for information-related errors in the application.
class InformationException(HTTPException):
    """
    Base class for information-related exceptions.
    Inherits from HTTPException to provide HTTP status codes and messages.
    This class can be extended to create specific information-related exceptions.
    """
    pass

# MARK: InformationErrorException
# Exception raised for errors related to information retrieval or processing.
class InformationErrorException(InformationException):
    """
    Exception raised for general information-related errors.
    Inherits from InformationException to provide a 500 Internal Server Error status code.

    General error in server processing of information-related operations.
    """
    def __init__(self, information: str, detail: str):
        # Define the error details.
        error_details = {
            "information": information,
            "detail": detail
        }

        # Call the parent constructor with a 500 status code and the message.
        super().__init__(status_code=500, detail=error_details)

# MARK: InformationClientException
# Exception raised for client-related errors in information retrieval or processing.
class InformationClientException(InformationException):
    """
    Exception raised for client-related errors in information retrieval or processing.
    Inherits from InformationException to provide a 400 Bad Request status code.

    Client error in information retrieval or processing, such as invalid input or request.
    """
    def __init__(self, information: str, detail: str):
        # Define the error details.
        error_details = {
            "information": information,
            "detail": detail
        }

        # Call the parent constructor with a 400 status code and the message.
        super().__init__(status_code=400, detail=error_details)