# MARK: Import
# Dependencies
import datetime
from pydantic import BaseModel, Field

# Modules
from config import EvIELTSConfig

# MARK: EvResponseMetadataModel
class EvResponseMetadataModel(BaseModel):
    # Properties
    code: int
    status: str
    message: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now())
    app_version: str = EvIELTSConfig.app_version