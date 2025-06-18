# MARK: Import
# Dependencies.
from fastapi import APIRouter, File, Form, Header, Request, UploadFile
from typing import Any, Optional

# Modules.
from app.core.models.response import ResponseModel
from app.core.services.response import standart_response
from app.evaluation.services.v1 import service as evaluation_service
from app.informations.services.v1 import service as information_service
from app.transcribe.services.v1 import service as transcribe_service
from app.user.services.v1 import service as user_service

# MARK: Router
# Create a new APIRouter instance for the information routes.
router = APIRouter(
    prefix="/api",
    tags=["Beta Testing Routes"],
)

# MARK: Test
# Define a test information route for the API to retrieve test information data.
@router.get("/information/test", response_model=ResponseModel)
async def get_test() -> ResponseModel:
    """
    Test information route for the API.

    Returns:
        ResponseModel: A standardized response model containing test information data.
    """
    # Fetch test information data using the service.
    test_data = await information_service.get_test_information_data()

    # Return the response using the standardized response function.
    return standart_response(
        data=test_data,
        code=200,
        status="Success",
        message="Test information data retrieved successfully."
    )

# MARK: Credit
# Define a user credit route for the API to retrieve user credit information.
@router.get("/information/credit", response_model=ResponseModel)
async def get_credit(authorization: Optional[str] = Header(None)) -> ResponseModel:
    """
    Get user credit route for the API.

    Args:
        authorization (Optional[str]): The authorization header for the request.

    Returns:
        ResponseModel: A standardized response model containing user credit information.
    """
    # Fetch user credit data using the service.
    credit_data = await user_service.get_credit(
        authorization=authorization
    )

    # Return the response using the standardized response function.
    return standart_response(
        data=credit_data,
        code=200,
        status="Success",
        message="User credit data retrieved successfully."
    )

# MARK: SpeakingIntroduction
# Define a speaking introduction information route for the API to retrieve speaking introduction data.
@router.get("/information/speaking-intro", response_model=ResponseModel)
async def get_speaking_introduction() -> ResponseModel:
    """
    Speaking introduction information route for the API.

    Returns:
        ResponseModel: A standardized response model containing speaking introduction information data.
    """
    # Fetch speaking introduction data using the service.
    speaking_intro_data = await information_service.get_speaking_introduction_information_data()

    # Return the response using the standardized response function.
    return standart_response(
        data=speaking_intro_data,
        code=200,
        status="Success",
        message="Speaking introduction data retrieved successfully."
    )

# MARK: SingleEvaluation
# Define a single evaluation route for the API to evaluate.
@router.post("/v3/evaluation", response_model=ResponseModel)
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
    result = await evaluation_service.get_single_evaluation(
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
@router.post("/v3/overall-feedback", response_model=ResponseModel)
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
    result = await evaluation_service.get_overall_evaluation(
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

# MARK: Transcribe
# Define a transcribe route for the API to transcribe audio files.
@router.post("/v3/transcribe", response_model=ResponseModel)
async def transcribe_audio(
    request: Request,
    file: Optional[UploadFile] = File(None),
    authorization: Optional[str] = Header(None),
    test_id: Optional[Any] = Form(None)
) -> ResponseModel:
    """
    Transcribe audio file.

    Args:
        request (Request): The HTTP request object.
        file (Optional[UploadFile]): The audio file to be transcribed.
        authorization (Optional[str]): The authorization header for the request.
        test_id (Optional[Any]): An optional test identifier for tracking.

    Returns:
        ResponseModel: The response model containing the transcription result.
    """
    # Call the transcribe service to process the audio file.
    result = await transcribe_service.transcribe(
        request=request,
        file=file,
        authorization=authorization,
        test_id=test_id
    )

    # Return the standardized response.
    return standart_response(
        data=result,
        code=200,
        status="Success",
        message="Audio transcription completed successfully."
    )