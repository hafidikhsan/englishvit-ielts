# MARK: Import
# Dependencies.
from pydantic import BaseModel, Field
from typing import Optional, Any

# Modules.
from config import EvIELTSConfig

# MARK: MetadataModel
# The metadata model for API responses of the EvIELTS API application.
class MetadataModel(BaseModel):
    """
    Metadata for the response of the EvIELTS API application.
    This model includes optional fields for timestamp, version, status, message, and code.
    """
    timestamp: Optional[str] = Field(default=None, description="Optional timestamp of the response")
    version: str = Field(default=EvIELTSConfig.app_version, description="Version of the application")
    status: Optional[str] = Field(default=None, description="Optional status of the response")
    message: Optional[str] = Field(default=None, description="Optional message for the response")
    code: Optional[int] = Field(default=None, description="Optional status code for the response")

# MARK: ResponseModel
# The base model for API responses of the EvIELTS API application.
class ResponseModel(BaseModel):
    """
    Base model for API responses of the EvIELTS API application.
    This model includes metadata and optional data for the response.
    """
    metadata: MetadataModel
    data: Optional[Any] = Field(default=None, description="Optional data for the response")