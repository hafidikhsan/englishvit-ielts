# MARK: Import
# Dependencies.
from fastapi import HTTPException

# MARK: UserException
# Base class for user-related exceptions inheriting from HTTPException. This class is used to 
# provide a consistent structure for user-related errors in the application.
class UserException(HTTPException):
    """
    Base class for user-related exceptions.
    Inherits from HTTPException to provide HTTP status codes and messages.
    This class can be extended to create specific user-related exceptions.
    """
    pass

# MARK: UserErrorException
# Exception raised for errors related to user retrieval or processing.
class UserErrorException(UserException):
    """
    Exception raised for general user-related errors.
    Inherits from UserException to provide a 500 Internal Server Error status code.

    General error in server processing of user-related operations.
    """
    def __init__(self, information: str, detail: str):
        # Define the error details.
        error_details = {
            "information": information,
            "detail": detail
        }

        # Call the parent constructor with a 500 status code and the message.
        super().__init__(status_code=500, detail=error_details)

# MARK: UserClientException
# Exception raised for client-related errors in user retrieval or processing.
class UserClientException(UserException):
    """
    Exception raised for client-related errors in user retrieval or processing.
    Inherits from UserException to provide a 400 Bad Request status code.

    Client error in user retrieval or processing, such as invalid input or request.
    """
    def __init__(self, information: str, detail: str):
        # Define the error details.
        error_details = {
            "information": information,
            "detail": detail
        }

        # Call the parent constructor with a 400 status code and the message.
        super().__init__(status_code=400, detail=error_details)

# MARK: UserServerException
# Exception raised for server-related errors in user retrieval or processing.
class UserServerException(UserException):
    """
    Exception raised for server-related errors in user retrieval or processing.
    Inherits from UserException to provide a 503 Service Unavailable status code.

    Server origin error in user retrieval or processing, such as database issues or 
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