# MARK: Import
# Modules.
from app.core.services.response import standart_response
from app.evaluation.models.exception import (
    EvaluationErrorException,
    EvaluationClientException,
    EvaluationServerException,
)

# MARK: ErrorException
# Define an exception handler for EvaluationErrorException.
def error_exception_handler(_, exc: EvaluationErrorException):
    """
    Exception handler for EvaluationErrorException.

    Args:
        _: The request object.
        exc: The EvaluationErrorException instance.

    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Error",
        message=f"An error occurred while processing the evaluation"
    )

# MARK: ClientException
# Define an exception handler for EvaluationClientException.
def client_exception_handler(_, exc: EvaluationClientException):
    """
    Exception handler for EvaluationClientException.

    Args:
        _: The request object.
        exc: The EvaluationClientException instance.

    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Client Error",
        message=f"A client error occurred while processing the evaluation"
    )

# MARK: ServerException
# Define an exception handler for EvaluationServerException.
def server_exception_handler(_, exc: EvaluationServerException):
    """
    Exception handler for EvaluationServerException.

    Args:
        _: The request object.
        exc: The EvaluationServerException instance.
    
    Returns:
        dict: A standardized error response.
    """
    # Return a standardized error response.
    return standart_response(
        data=exc.detail,
        code=exc.status_code,
        status="Server Error",
        message=f"A server error occurred while processing the evaluation"
    )