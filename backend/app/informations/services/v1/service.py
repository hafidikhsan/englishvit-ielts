# MARK: Import
# Dependencies.
from fastapi import Request
import json
import logging
import os

# Modules.
from app.core.services.response import standart_response
from app.informations.models.exception import InformationErrorException, InformationClientException

# MARK: Variables
# Define some constants for information services.
_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
_information_test_file_path = os.path.join(_base_dir, "public", "json", "information_test.json")
_speaking_introduction_file_path = os.path.join(_base_dir, "public", "json", "speaking_simulation_intro.json")

# MARK: Test
# Get test information data service.
async def get_test_information_data() -> dict:
    """
    Service to retrieve test information data.
    
    Returns:
        dict: A dictionary containing test information data.
    """
    try:
        try:
            # Open the JSON file containing test information data.
            with open(_information_test_file_path, "r", encoding="utf-8") as f:
                # Load the JSON data from the file.
                data = json.load(f)

            # Log the test data retrieval for debugging purposes.
            logging.info(f"Test information data retrieved")

            # Return the retrieved data in a dictionary format.
            return {"information": data}
        
        except FileNotFoundError:
            # Log the error if the file is not found.
            raise Exception(f"File not found: {_information_test_file_path}")
        
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error retrieving test information data: {str(error)}")

        # Handle any exceptions that occur during data retrieval.
        raise InformationErrorException(
            information="GET -> Test Information Data",
            detail=str(error)
        )
    
# Update test information data service.
async def update_test_information_data(request: Request) -> dict:
    """
    Service to update test information data.

    Args:
        request (Request): The request object containing the JSON data to update.
    
    Returns:
        dict: A dictionary containing updated test information data.
    """
    # Check if the request content type is JSON.
    content_type = request.headers.get("content-type", "")

    # If the content type is not JSON, raise an exception.
    if "application/json" not in content_type:
        # Log the error for debugging purposes.
        logging.error("Content-Type must be application/json")

        # Raise an exception if the content type is not JSON.
        raise InformationClientException(
            information="UPDATE -> Test Information Data",
            detail="Content-Type must be application/json"
        )
    
    try:
        try:
            # Read the JSON data from the request body.
            data = await request.json()

            # Open the JSON file containing test information data.
            with open(_information_test_file_path, "w") as f:
                # Write the updated data back to the file.
                json.dump(data, f, indent=4)

            # Log the test data update for debugging purposes.
            logging.info(f"Test information data updated")

            # Return the updated data in a dictionary format.
            return {"information": data}
        
        except FileNotFoundError:
            # Log the error if the file is not found.
            raise Exception(f"File not found: {_information_test_file_path}")
        
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error updating test information data: {str(error)}")

        # Handle any exceptions that occur during data update.
        raise InformationErrorException(
            information="UPDATE -> Test Information Data",
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
        try:
            # Open the JSON file containing speaking introduction information data.
            with open(_speaking_introduction_file_path, "r", encoding="utf-8") as f:
                # Load the JSON data from the file.
                data = json.load(f)

            # Log the speaking introduction data retrieval for debugging purposes.
            logging.info(f"Speaking introduction information data retrieved")

            # Return the retrieved data in a dictionary format.
            return {"information": data}
        
        except FileNotFoundError:
            # Log the error if the file is not found.
            raise Exception(f"File not found: {_speaking_introduction_file_path}")
        
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error retrieving speaking introduction information data: {str(error)}")

        # Handle any exceptions that occur during data retrieval.
        raise InformationErrorException(
            information="GET -> Speaking Introduction Information Data",
            detail=str(error)
        )
    
# Update speaking introduction information data service.
async def update_speaking_introduction_information_data(request: Request) -> dict:
    """
    Service to update speaking introduction information data.

    Args:
        request (Request): The request object containing the JSON data to update.
    
    Returns:
        dict: A dictionary containing updated speaking introduction information data.
    """
    # Check if the request content type is JSON.
    content_type = request.headers.get("content-type", "")

    # If the content type is not JSON, raise an exception.
    if "application/json" not in content_type:
        # Log the error for debugging purposes.
        logging.error("Content-Type must be application/json")

        # Raise an exception if the content type is not JSON.
        raise InformationClientException(
            information="UPDATE -> Speaking Introduction Information Data",
            detail="Content-Type must be application/json"
        )
    
    try:
        try:
            # Read the JSON data from the request body.
            data = await request.json()

            # Open the JSON file containing speaking introduction information data.
            with open(_speaking_introduction_file_path, "w") as f:
                # Write the updated data back to the file.
                json.dump(data, f, indent=4)

            # Log the speaking introduction data update for debugging purposes.
            logging.info(f"Speaking introduction information data updated")

            # Return the updated data in a dictionary format.
            return {"information": data}
        
        except FileNotFoundError:
            # Log the error if the file is not found.
            raise Exception(f"File not found: {_speaking_introduction_file_path}")

    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error updating speaking introduction information data: {str(error)}")

        # Handle any exceptions that occur during data update.
        raise InformationErrorException(
            information="UPDATE -> Speaking Introduction Information Data",
            detail=str(error)
        )
    
# MARK: ExceptionHandler
# Define an exception handler for InformationErrorException.
async def information_error_exception_handler(_, exc: InformationErrorException):
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

# Define an exception handler for InformationClientException.
async def information_client_exception_handler(_, exc: InformationClientException):
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