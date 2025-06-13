# MARK: Import
# Dependencies.
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import Any

# Modules.
from app.core.models.response import ResponseModel, MetadataModel

# MARK: StandartResponse
# Function to create a standardized API response for the EvIELTS API application.
def standart_response(data: Any, code: int, status: str, message: str) -> JSONResponse:
    """
    Constructs a standardized JSON response for the API with metadata and data fields.
    This function is used to create a consistent response format across the EvIELTS API application.
    Args:
        data (Any): The data to include in the response.
        code (int): The HTTP status code for the response.
        status (str): The status of the response (e.g., "Success", "Error").
        message (str): An optional message for the response.
    Returns:
        JSONResponse: A FastAPI JSONResponse object containing the response data.
    """
    # Create metadata for the response.
    metadata = MetadataModel(
        code=code,
        status=status,
        message=message,
        timestamp=datetime.now().isoformat()
    )

    # Create the response model.
    response = ResponseModel(
        metadata=metadata,
        data=data
    )

    # Return the JSON response with the response model.
    return JSONResponse(content=response.dict(), status_code=code, media_type="application/json")