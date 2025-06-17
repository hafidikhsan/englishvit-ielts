# MARK: Import
# Dependencies.
from fastapi import Form, Header
import logging
from typing import Any, Optional

# Modules.
from app.core.services.response import standart_response
from app.user.models.exception import UserErrorException, UserClientException, UserServerException

# MARK: Variables
# Define some constants for user services.
_user_credit = 2

# MARK: Credit
# Get user credit information service.
async def get_credit(authorization: Optional[str] = Header(None)) -> dict:
    """
    Service to retrieve user credit information data from the origin server.

    Args:
        authorization (Optional[str]): The authorization header for the request.
    
    Returns:
        dict: A dictionary containing user credit information.
    """
    # Check if the authorization header is provided.
    if not authorization:
        # Log the error for debugging purposes.
        logging.error("Authorization header is missing")
        
        # Raise an exception if the authorization header is not provided.
        raise UserClientException(
            information="GET -> User Credit",
            detail="Authorization header is required"
        )
    
    try:
        # Log the user credit retrieval for debugging purposes.
        logging.info("User credit information retrieved")
        
        # Set user credit data.
        return {"information": _user_credit}
    
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error retrieving user credit information: {error}")

        # Handle any exceptions that occur during data retrieval.
        raise UserErrorException(
            information="GET -> User Credit",
            detail=str(error)
        )
    
# Update user credit information service.
async def update_credit(authorization: Optional[str] = Header(None), new_credit: Optional[Any] = Form(None)) -> dict:
    """
    Service to update user credit information data from the origin server.

    Args:
        authorization (Optional[str]): The authorization header for the request.
        new_credit (Optional[Any]): The new credit value to be updated.

    Returns:
        dict: A dictionary containing updated user credit information.
    """
    # Check if the authorization header is provided.
    if not authorization:
        # Log the error for debugging purposes.
        logging.error("Authorization header is missing")
        
        # Raise an exception if the authorization header is not provided.
        raise UserClientException(
            information="UPDATE -> User Credit",
            detail="Authorization header is required"
        )
    
    # Check if the new credit value is provided.
    if new_credit is None:
        # Log the error for debugging purposes.
        logging.error("New credit value is missing")
        
        # Raise an exception if the new credit value is not provided.
        raise UserClientException(
            information="UPDATE -> User Credit",
            detail="New credit value is required"
        )
    
    # Try to parse the new credit value.
    try:
        # Attempt to convert the new credit value to an integer.
        new_credit = int(new_credit)
        
        # Check if the new credit value is negative.
        if new_credit < 0:
            # Log the error for debugging purposes.
            logging.error("New credit value cannot be negative")
            
            # Raise an exception if the new credit value is negative.
            raise UserClientException(
                information="UPDATE -> User Credit",
                detail="New credit value cannot be negative"
            )
    
    except ValueError:
        # Log the error for debugging purposes.
        logging.error("Invalid new credit value provided")
        
        # Raise an exception if the new credit value is not a valid integer.
        raise UserClientException(
            information="UPDATE -> User Credit",
            detail="New credit value must be a valid integer"
        )
    
    try:
        # Get the global user credit variable.
        global _user_credit

        # Update the user credit information.
        _user_credit = new_credit

        # Log the user credit update for debugging purposes.
        logging.info("User credit information updated")
        
        # Set user credit data.
        return {"information": _user_credit}
    
    except Exception as error:
        # Log the error for debugging purposes.
        logging.error(f"Error updating user credit information: {error}")

        # Handle any exceptions that occur during data retrieval.
        raise UserServerException(
            information="UPDATE -> User Credit",
            detail=str(error)
        )

# MARK: ExceptionHandler
# Define an exception handler for UserErrorException.
async def user_error_exception_handler(_, exc: UserErrorException):
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

# Define an exception handler for UserClientException.
async def user_client_exception_handler(_, exc: UserClientException):
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

# Define an exception handler for UserServerException.
async def user_server_exception_handler(_, exc: UserServerException):
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