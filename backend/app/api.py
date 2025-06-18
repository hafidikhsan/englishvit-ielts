# MARK: Import
# Dependencies.
from fastapi import FastAPI

# Modules.
from app.beta.controllers import routes as beta_routes
from app.evaluation.controllers.v1 import routes as v1_evaluation
from app.informations.controllers.v1 import routes as v1_information
from app.transcribe.controllers.v1 import routes as v1_transcribe
from app.user.controllers.v1 import routes as v1_user

# MARK: RegisterRoutes
# Function to register all API routes.
def register_routes(app: FastAPI) -> None:
    """
    Registers all API routes with the FastAPI application instance in this Englishvit IELTS API application.
    
    Args:
        app (FastAPI): The FastAPI application instance to register routes with.
    """
    # Include beta testing routes.
    app.include_router(beta_routes.router)
    # Include version 1 evaluation routes.
    app.include_router(v1_evaluation.router)
    # Include version 1 information routes.
    app.include_router(v1_information.router)
    # Include version 1 transcribe routes.
    app.include_router(v1_transcribe.router)
    # Include version 1 user routes.
    app.include_router(v1_user.router)