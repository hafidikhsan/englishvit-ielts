# MARK: Import
# Dependencies.
from fastapi import FastAPI

# Modules.
from app.informations.controllers.v1 import routes as v1_information_routes
from app.informations.services.v1 import service
from app.informations.models.exception import InformationErrorException

# MARK: RegisterRoutes
# Function to register all API routes.
def register_routes(app: FastAPI) -> None:
    """
    Registers all API routes with the FastAPI application instance.
    
    Args:
        app (FastAPI): The FastAPI application instance to register routes with.
    """
    # Include version 1 information routes.
    app.include_router(v1_information_routes.router)

    # Register exception handlers.
    app.add_exception_handler(InformationErrorException, service.information_error_exception_handler)