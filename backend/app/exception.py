# MARK: Import
# Dependencies.
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Modules.
from app.core.services import exception as core
from app.evaluation.services import exception as evaluation
from app.informations.services import exception as information
from app.transcribe.services import exception as transcribe
from app.user.services import exception as user
from app.evaluation.models.exception import (
    EvaluationErrorException, 
    EvaluationClientException, 
    EvaluationServerException
)
from app.informations.models.exception import (
    InformationErrorException, 
    InformationClientException
)
from app.transcribe.models.exception import (
    TranscribeErrorException, 
    TranscribeClientException, 
    TranscribeServerException
)
from app.user.models.exception import (
    UserErrorException, 
    UserClientException, 
    UserServerException
)

# MARK: RegisterExceptionHandlers
# Function to register all exception handlers with the FastAPI application instance.
def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers all exception handlers with the FastAPI application instance in this Englishvit IELTS API application.

    Args:
        app (FastAPI): The FastAPI application instance to register exception handlers with.
    """
    # Register core exception handlers.
    app.add_exception_handler(StarletteHTTPException, core.custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, core.validation_exception_handler)
    # Register exception handlers for evaluation-related exceptions.
    app.add_exception_handler(EvaluationErrorException, evaluation.error_exception_handler)
    app.add_exception_handler(EvaluationClientException, evaluation.client_exception_handler)
    app.add_exception_handler(EvaluationServerException, evaluation.server_exception_handler)
    # Register exception handlers for information-related exceptions.
    app.add_exception_handler(InformationErrorException, information.error_exception_handler)
    app.add_exception_handler(InformationClientException, information.client_exception_handler)
    # Register exception handlers for transcribe-related exceptions.
    app.add_exception_handler(TranscribeErrorException, transcribe.error_exception_handler)
    app.add_exception_handler(TranscribeClientException, transcribe.client_exception_handler)
    app.add_exception_handler(TranscribeServerException, transcribe.server_exception_handler)
    # Register exception handlers for user-related exceptions.
    app.add_exception_handler(UserErrorException, user.error_exception_handler)
    app.add_exception_handler(UserClientException, user.client_exception_handler)
    app.add_exception_handler(UserServerException, user.server_exception_handler)