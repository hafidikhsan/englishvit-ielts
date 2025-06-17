# MARK: Import
# Dependencies.
from fastapi import APIRouter, Form, Header
from typing import Any, Optional 

# Modules.
from app.core.models.response import ResponseModel
from app.core.services.response import standart_response
from app.user.services.v1 import service

# MARK: Router
# Create a new APIRouter instance for the user routes.
router = APIRouter(
    prefix="/api/v1/user",
    tags=["User Routes Version 1"],
)

# MARK: Variables
# Define some constants for the API routes.
_credit_path = "/credit"

# MARK: Credit
# Define a user credit route for the API to retrieve user credit information.
@router.get(_credit_path, response_model=ResponseModel)
async def get_credit(authorization: Optional[str] = Header(None)) -> ResponseModel:
    """
    Get user credit route for the API.

    Args:
        authorization (Optional[str]): The authorization header for the request.

    Returns:
        ResponseModel: A standardized response model containing user credit information.
    """
    # Fetch user credit data using the service.
    credit_data = await service.get_credit(
        authorization=authorization
    )

    # Return the response using the standardized response function.
    return standart_response(
        data=credit_data,
        code=200,
        status="Success",
        message="User credit data retrieved successfully."
    )

# Define a user credit route for the API to update user credit information.
@router.post(_credit_path, response_model=ResponseModel)
async def update_credit(authorization: Optional[str] = Header(None), new_credit: Optional[Any] = Form(None)) -> ResponseModel:
    """
    Update user credit route for the API.

    Args:
        authorization (Optional[str]): The authorization header for the request.
        new_credit (Optional[Any]): The new credit value to update.

    Returns:
        ResponseModel: A standardized response model containing updated user credit information.
    """
    # Update user credit data using the service.
    updated_data = await service.update_credit(
        authorization=authorization,
        new_credit=new_credit
    )

    # Return the response using the standardized response function.
    return standart_response(
        data=updated_data,
        code=200,
        status="Success",
        message="User credit data updated successfully."
    )