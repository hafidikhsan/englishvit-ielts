# MARK: Import
# Dependencies.
from fastapi import APIRouter

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

# MARK: Test
# Define a test information route for the API.
@router.get("/test", response_model=ResponseModel)
async def test() -> ResponseModel:
    """
    Test information route for the API.
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

# MARK: SpeakingIntroduction
# Define a speaking introduction information route for the API.
@router.get("/speaking-introduction", response_model=ResponseModel)
async def speaking_introduction() -> ResponseModel:
    """
    Speaking introduction information route for the API.
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