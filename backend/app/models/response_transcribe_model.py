# MARK: Import
# Dependencies
from pydantic import BaseModel

# MARK: EvResponseTranscribeModel
class EvResponseTranscribeModel(BaseModel):
    # Properties
    transcribe: str
    word_timestamp: str