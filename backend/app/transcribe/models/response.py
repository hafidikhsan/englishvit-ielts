# MARK: Import
# Dependencies.
from pydantic import BaseModel, Field
from typing import Optional

# MARK: TranscribeResponseModel
# The base model for transcribe-related API responses of the EvIELTS API application.
class TranscribeResponseModel(BaseModel):
    """
    Base model for transcribe-related API responses of the EvIELTS API application.
    """
    transcribe: Optional[str] = Field(default=None, description="Transcription text")
    word_timestamp: Optional[str] = Field(default=None, description="Word-level timestamps for the transcription")