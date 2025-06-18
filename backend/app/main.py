# MARK: Import
# Dependencies.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Modules.
from config import EvIELTSConfig
from .logging import configure_logging, LogLevels
from .api import register_routes
from .exception import register_exception_handlers
from app.core.services.response import standart_response
from app.transcribe.services.v1 import service as v1_transcribe_service

# MARK: ConfigureLogging
configure_logging(log_level=LogLevels.info)

# MARK: FastAPIInstance
# Create FastAPI instance with configuration.
app = FastAPI(
    title=EvIELTSConfig.app_name,
    version=EvIELTSConfig.app_version,
)

# MARK: CORS
# Configure CORS middleware to allow cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MARK: StartupEvent
# Define a startup event in the EvIELTS API application.
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler for the EvIELTS API application.

    This function is called when the application starts up.
    """
    # Load the Silero VAD model during application startup.
    model = v1_transcribe_service.load_silero_vad_model()

    # Store the model in the application state for later use.
    app.state.vad_model = model

# MARK: RegisterRoutes
# Function to register all API routes.
register_routes(app)

# MARK: RegisterExceptionHandlers
# Function to register exception handlers for the application.
register_exception_handlers(app)

# MARK: RootEndpoint
# Define the root endpoint for the API.
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    # Return a welcome message with API version information.
    return standart_response(
        data={
            "message": "Welcome to the Englishvit IELTS API!", 
            "versions": {
                "v1": "api/v1",
            }
        },
        code=200,
        status="Success",
        message="Englishvit IELTS API is running successfully."
    )