# MARK: Import
# Dependencies.
from fastapi import APIRouter, File, Form, Header, UploadFile
from typing import Any, Optional

# Modules.
from app.core.models.response import ResponseModel
from app.core.services.response import standart_response
from app.evaluation.services.v1 import service

# MARK: Router
# Create a new APIRouter instance for the evaluation routes.
router = APIRouter(
    prefix="/api/v1/evaluation",
    tags=["Evaluation Routes Version 1"],
)

# MARK: Variables
# Define some constants for the API routes.
_single = "/single"
_overall = "/overall"
_info = "/info"
_settings = "/settings"

# MARK: SingleEvaluation
# Define a single evaluation route for the API to evaluate.
@router.post(_single, response_model=ResponseModel)
async def get_single_evaluation(
    authorization: Optional[str] = Header(None),
    test_id: Optional[Any] = Form(None),
    question: Optional[str] = Form(None),
    answer: Optional[str] = Form(None),
) -> ResponseModel:
    """
    Evaluate a single evaluation.

    Args:
        authorization (Optional[str]): The authorization header for the request.
        test_id (Optional[Any]): An optional test identifier for tracking.
        question (Optional[str]): The question associated with the evaluation.
        answer (Optional[str]): The answer provided for the evaluation.

    Returns:
        ResponseModel: The response model containing the evaluation result.
    """
    # Call the evaluation service to perform the single evaluation.
    result = await service.get_single_evaluation(
        authorization=authorization,
        test_id=test_id,
        question=question,
        answer=answer
    )

    # Return the standardized response.
    return standart_response(
        data=result,
        code=200,
        status="Success",
        message="Single evaluation completed successfully."
    )

# MARK: OverallEvaluation
# Define an overall evaluation route for the API to evaluate.
@router.post(_overall, response_model=ResponseModel)
async def get_overall_evaluation(
    authorization: Optional[str] = Header(None),
    session_id: Optional[Any] = Form(None),
    finished: Optional[Any] = Form(None),
    histories: Optional[str] = Form(None),
) -> ResponseModel:
    """
    Evaluate an overall evaluation.

    Args:
        authorization (Optional[str]): The authorization header for the request.
        session_id (Optional[Any]): An optional session identifier for tracking.
        finished (Optional[Any]): An optional flag indicating if the evaluation is finished.
        histories (Optional[str]): An optional string containing the evaluation histories.

    Returns:
        ResponseModel: The response model containing the evaluation result.
    """
    # Call the evaluation service to perform the overall evaluation.
    result = await service.get_overall_evaluation(
        authorization=authorization,
        session_id=session_id,
        finished=finished,
        histories=histories
    )

    # Return the standardized response.
    return standart_response(
        data=result,
        code=200,
        status="Success",
        message="Overall evaluation completed successfully."
    )

# MARK: ServiceInformation
# Define a route to get information about the evaluation service.
@router.get(_info, response_model=ResponseModel)
async def get_service_info() -> ResponseModel:
    """
    Get information about the evaluation service.

    Returns:
        ResponseModel: The response model containing service information.
    """
    # Call the evaluation service to get information.
    result = await service.get_service_info()

    # Return the standardized response.
    return standart_response(
        data=result,
        code=200,
        status="Success",
        message="Evaluation service information retrieved successfully."
    )

# MARK: SettingsOpenAIChatModelName
# Define a route to update the OpenAI chat model name.
@router.post(_settings + "/chat", response_model=ResponseModel)
async def update_openai_chat_model_name(
    model_name: Optional[Any] = Form(None)
) -> ResponseModel:
    """
    Update the OpenAI chat model name.

    Args:
        model_name (Optional[Any]): The name of the OpenAI chat model to be set.

    Returns:
        ResponseModel: The response model containing chat model settings.
    """
    # Call the evaluation service to update the chat model name.
    settings = await service.update_openai_chat_model_name(
        model_name=model_name
    )

    # Return the standardized response.
    return standart_response(
        data=settings,
        code=200,
        status="Success",
        message="Chat model name updated successfully."
    )

# MARK: SettingsSinglePrompt
# Define a route to update the single evaluation prompt.
@router.post(_settings + "/single-prompt", response_model=ResponseModel)
async def update_single_prompt(
    file: Optional[UploadFile] = File(None),
) -> ResponseModel:
    """
    Update the single evaluation prompt.

    Args:
        file (Optional[UploadFile]): The new single evaluation prompt file to be set.

    Returns:
        ResponseModel: The response model containing the updated single evaluation prompt.
    """
    # Call the evaluation service to update the single evaluation prompt.
    updated_prompt = await service.update_single_prompt(file=file)

    # Return the standardized response.
    return standart_response(
        data=updated_prompt,
        code=200,
        status="Success",
        message="Single evaluation prompt updated successfully."
    )

# MARK: SettingsOverallPrompt
# Define a route to update the overall evaluation prompt.
@router.post(_settings + "/overall-prompt", response_model=ResponseModel)
async def update_overall_prompt(
    file: Optional[UploadFile] = File(None),
) -> ResponseModel:
    """
    Update the overall evaluation prompt.

    Args:
        file (Optional[UploadFile]): The new overall evaluation prompt file to be set.

    Returns:
        ResponseModel: The response model containing the updated overall evaluation prompt.
    """
    # Call the evaluation service to update the overall evaluation prompt.
    updated_prompt = await service.update_overall_prompt(file=file)

    # Return the standardized response.
    return standart_response(
        data=updated_prompt,
        code=200,
        status="Success",
        message="Overall evaluation prompt updated successfully."
    )