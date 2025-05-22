# MARK: Import
# Dependencies
from pydantic import BaseModel

# Modules
from app.models.response_metadata_model import EvResponseMetadataModel

# MARK: EvResponseModel
class EvResponseModel(BaseModel):
    # Properties
    metadata: EvResponseMetadataModel
    data: dict