# MARK: Import
# Dependencies.
from fastapi import FastAPI

# Modules.
from app.informations.controllers.v1 import routes as v1_information_routes
from app.informations.models.exception import InformationErrorException, InformationClientException
from app.informations.services.v1 import service as v1_information_service
from app.user.controllers.v1 import routes as v1_user_routes
from app.user.models.exception import UserErrorException, UserClientException, UserServerException
from app.user.services.v1 import service as v1_user_service

# MARK: RegisterRoutes
# Function to register all API routes.
def register_routes(app: FastAPI) -> None:
    """
    Registers all API routes with the FastAPI application instance.
    
    Args:
        app (FastAPI): The FastAPI application instance to register routes with.
    """
    # All routes.
    # Include version 1 information routes.
    app.include_router(v1_information_routes.router)
    # Include version 1 user routes.
    app.include_router(v1_user_routes.router)

    # All exception handlers.
    # Register exception handlers for information-related exceptions.
    app.add_exception_handler(InformationErrorException, v1_information_service.information_error_exception_handler)
    app.add_exception_handler(InformationClientException, v1_information_service.information_client_exception_handler)
    # Register exception handlers for user-related exceptions.
    app.add_exception_handler(UserErrorException, v1_user_service.user_error_exception_handler)
    app.add_exception_handler(UserClientException, v1_user_service.user_client_exception_handler)
    app.add_exception_handler(UserServerException, v1_user_service.user_server_exception_handler)