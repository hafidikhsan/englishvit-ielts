# MARK: Import
# # Modules.
from app.core.services.response import standart_response
from app.informations.models.exception import (
    InformationErrorException, 
    InformationClientException
)

# MARK: ErrorException
# Define an exception handler for InformationErrorException.
async def error_exception_handler(_, exc: InformationErrorException):
    """
    Exception handler for InformationErrorException.
    
    Args:
        _: The request object.
        exc (InformationErrorException): The exception instance.
    
    Returns:
        ResponseModel: A standardized response model with error details.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Error",
        message=f"An error occurred while processing the information"
    )

# MARK: ClientException
# Define an exception handler for InformationClientException.
async def client_exception_handler(_, exc: InformationClientException):
    """
    Exception handler for InformationClientException.
    
    Args:
        _: The request object.
        exc (InformationClientException): The exception instance.
    
    Returns:
        ResponseModel: A standardized response model with error details.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Client Error",
        message=f"A client error occurred while processing the information"
    )