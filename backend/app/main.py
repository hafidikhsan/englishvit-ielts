# MARK: Import
# Dependencies.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Modules.
from config import EvIELTSConfig
from .logging import configure_logging, LogLevels
from .api import register_routes
from app.core.services.response import standart_response

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

# MARK: RegisterRoutes
# Function to register all API routes.
register_routes(app)

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