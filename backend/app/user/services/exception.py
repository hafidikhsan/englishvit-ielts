# MARK: Imports
# Modules.
from app.core.services.response import standart_response
from app.user.models.exception import (
    UserErrorException, 
    UserClientException, 
    UserServerException
)

# MARK: ErrorException
# Define an exception handler for UserErrorException.
async def error_exception_handler(_, exc: UserErrorException):
    """
    Exception handler for UserErrorException.
    
    Args:
        _: The request object.
        exc: The UserErrorException instance.
    
    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Error",
        message=f"An error occurred while processing the user"
    )

# MARK: ClientException
# Define an exception handler for UserClientException.
async def client_exception_handler(_, exc: UserClientException):
    """
    Exception handler for UserClientException.
    
    Args:
        _: The request object.
        exc: The UserClientException instance.
    
    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Client Error",
        message=f"A client error occurred while processing the user"
    )

# MARK: ServerException
# Define an exception handler for UserServerException.
async def server_exception_handler(_, exc: UserServerException):
    """
    Exception handler for UserServerException.
    
    Args:
        _: The request object.
        exc: The UserServerException instance.
    
    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Server Error",
        message=f"A server error occurred while processing the user"
    )