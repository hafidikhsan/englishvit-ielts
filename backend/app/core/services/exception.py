# MARK: Import
# Dependencies.
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Modules.
from app.core.services.response import standart_response

# MARK: CustomHTTPExceptionHandler
# Function to handle custom HTTP exceptions and return standardized error responses.
def custom_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handles custom HTTP exceptions and returns a standardized error response.

    Args:
        request (Request): The incoming request object.
        exc (StarletteHTTPException): The exception that was raised.

    Returns:
        JSONResponse: A standardized error response in JSON format.
    """
    # Check if the exception is a 404 Not Found error.
    if exc.status_code == 404:
        # Return a standardized 404 Not Found response.
        return standart_response(
            data={
                "detail": "The requested resource was not found.",
                "path": request.url.path,
                "method": request.method,
                "exception": str(exc)
            },
            code=404,
            status="Not Found",
            message="The requested URL was not found on the server."
        )
    
    # Return default for other errors
    return standart_response(
        data={
            "detail": "An unexpected error occurred.",
            "path": request.url.path,
            "method": request.method,
            "exception": str(exc)
        },
        code=exc.status_code,
        status="Error",
        message=f"An error occurred while processing the request"
    )

# MARK: ValidationExceptionHandler
# Function to handle validation exceptions and return standardized error responses.
def validation_exception_handler(request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles validation exceptions and returns a standardized error response.

    This will be called when a request validation error occurs, such as when
    the request body does not match the expected schema.

    Args:
        request (Request): The incoming request object.
        exc (RequestValidationError): The exception that was raised.

    Returns:
        JSONResponse: A standardized error response in JSON format.
    """
    # Return a standardized error response.
    return standart_response(
        data={
            "detail": "An unexpected error occurred.",
            "path": request.url.path,
            "method": request.method,
            "exception": str(exc)
        },
        code=400,
        status="Client Error",
        message=f"A client error occurred while processing the request"
    )