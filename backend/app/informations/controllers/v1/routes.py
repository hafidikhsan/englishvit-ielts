# MARK: Import
# Dependencies.
from fastapi import APIRouter, Request

# Modules.
from app.core.models.response import ResponseModel
from app.core.services.response import standart_response
from app.informations.services.v1 import service

# MARK: Router
# Create a new APIRouter instance for the information routes.
router = APIRouter(
    prefix="/api/v1/informations",
    tags=["Informations Routes Version 1"],
)

# MARK: Variables
# Define some constants for the API routes.
_test_path = "/test"
_speaking_introduction_path = "/speaking-introduction"

# MARK: Test
# Define a test information route for the API to retrieve test information data.
@router.get(_test_path, response_model=ResponseModel)
async def get_test() -> ResponseModel:
    """
    Test information route for the API.

    Returns:
        ResponseModel: A standardized response model containing test information data.
    """
    # Fetch test information data using the service.
    test_data = await service.get_test_information_data()

    # Return the response using the standardized response function.
    return standart_response(
        data=test_data,
        code=200,
        status="Success",
        message="Test information data retrieved successfully."
    )

# Define a test information route for the API to update test information data.
@router.post(_test_path, response_model=ResponseModel)
async def update_test(request: Request) -> ResponseModel:
    """
    Update test information route for the API.

    Args:
        request (Request): The request object containing the JSON data to update.

    Returns:
        ResponseModel: A standardized response model containing the updated test information data.
    """
    # Update test information data using the service.
    updated_data = await service.update_test_information_data(
        request=request
    )

    # Return the response using the standardized response function.
    return standart_response(
        data=updated_data,
        code=200,
        status="Success",
        message="Test information data updated successfully."
    )

# MARK: SpeakingIntroduction
# Define a speaking introduction information route for the API to retrieve speaking introduction data.
@router.get(_speaking_introduction_path, response_model=ResponseModel)
async def get_speaking_introduction() -> ResponseModel:
    """
    Speaking introduction information route for the API.

    Returns:
        ResponseModel: A standardized response model containing speaking introduction information data.
    """
    # Fetch speaking introduction data using the service.
    speaking_intro_data = await service.get_speaking_introduction_information_data()

    # Return the response using the standardized response function.
    return standart_response(
        data=speaking_intro_data,
        code=200,
        status="Success",
        message="Speaking introduction data retrieved successfully."
    )

# Define a speaking introduction information route for the API to update speaking introduction data.
@router.post(_speaking_introduction_path, response_model=ResponseModel)
async def update_speaking_introduction(request: Request) -> ResponseModel:
    """
    Update speaking introduction information route for the API.

    Args:
        request (Request): The request object containing the JSON data to update.
        
    Returns:
        ResponseModel: A standardized response model containing the updated speaking introduction information data.
    """
    # Update speaking introduction data using the service.
    updated_data = await service.update_speaking_introduction_information_data(
        request=request
    )

    # Return the response using the standardized response function.
    return standart_response(
        data=updated_data,
        code=200,
        status="Success",
        message="Speaking introduction data updated successfully."
    )