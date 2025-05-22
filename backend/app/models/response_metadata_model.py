# MARK: Import
# Dependencies
from datetime import datetime
from pydantic import BaseModel, Field

# Modules
from config import EvIELTSConfig

# MARK: EvResponseMetadataModel
class EvResponseMetadataModel(BaseModel):
    # Properties
    code: int
    status: str
    message: str
    # timestamp: datetime | None
    app_version: str = EvIELTSConfig.app_version