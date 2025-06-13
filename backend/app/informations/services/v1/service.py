# MARK: Import
# Dependencies.
import logging

# Modules.
from app.core.services.response import standart_response
from app.informations.models.exception import InformationErrorException

# MARK: Test
# Get test information data service.
async def get_test_information_data() -> dict:
    """
    Service to retrieve test information data.
    
    Returns:
        dict: A dictionary containing test information data.
    """
    try:
        # Simulate fetching test information data.
        test_data = {
            "test_name": "EvIELTS Test",
            "test_date": "2023-10-01",
            "test_location": "Online",
            "test_duration": "2 hours"
        }

        # Log the test data retrieval for debugging purposes.
        logging.info(f"Test information data retrieved")

        # Return the test data.
        return test_data
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error retrieving test information data: {str(error)}")

        # Handle any exceptions that occur during data retrieval.
        raise InformationErrorException(
            information="Test Information Data",
            detail=str(error)
        )

# MARK: SpeakingIntroduction
# Get speaking introduction information data service.
async def get_speaking_introduction_information_data() -> dict:
    """
    Service to retrieve speaking introduction information data.
    
    Returns:
        dict: A dictionary containing speaking introduction information data.
    """
    try:
        # Simulate fetching speaking introduction information.
        speaking_info = {
            "introduction": "Welcome to the EvIELTS Speaking Test.",
            "instructions": "Please introduce yourself and talk about your interests."
        }

        # Simulate an error for testing purposes (comment this line in production).
        raise Exception("Simulated error for testing purposes")
    
        # Log the speaking introduction information retrieval for debugging purposes.
        logging.info(f"Speaking introduction information data retrieved")
        
        # Return the speaking introduction information.
        return speaking_info
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error retrieving speaking introduction information data: {str(error)}")

        # Handle any exceptions that occur during data retrieval.
        raise InformationErrorException(
            information="Speaking Introduction Information Data",
            detail=str(error)
        )
    
# MARK: ExceptionHandler
# Define an exception handler for InformationErrorException.
async def information_error_exception_handler(request, exc: InformationErrorException):
    """
    Exception handler for InformationErrorException.
    
    Args:
        request: The request object.
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