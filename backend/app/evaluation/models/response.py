# MARK: Import
# Dependencies.
from pydantic import BaseModel

# MARK: ResponseSingleFeedbackModel
# Model for feedback on the single evaluation data response.
class ResponseSingleFeedbackModel(BaseModel):
    """
    Model for feedback on the single evaluation data response.
    """
    feedback: str
    candidate_answer: str
    points: list[str]

# MARK: ResponseSingleDataModel
# Model for data on the single evaluation response.
class ResponseSingleDataModel(BaseModel):
    """
    Model for data on the single evaluation response.
    """
    final_band: float
    readable_feedback: ResponseSingleFeedbackModel

# MARK: ResponseSingleModel
# Model for the single evaluation response.
class ResponseSingleModel(BaseModel):
    """
    Model for the single evaluation response.
    """
    fluency: ResponseSingleDataModel
    lexical: ResponseSingleDataModel
    grammar: ResponseSingleDataModel
    pronunciation: ResponseSingleDataModel

# MARK: ResponseOverallDataModel
# Model for data on the overall evaluation response.
class ResponseOverallDataModel(BaseModel):
    """
    Model for data on the overall evaluation response.
    """
    final_band: float
    readable_feedback: str
    tips_feedback: str

# MARK: ResponseOverallModel
# Model for the overall evaluation response.
class ResponseOverallModel(BaseModel):
    """
    Model for the overall evaluation response.
    """
    overall: ResponseOverallDataModel
    fluency: ResponseOverallDataModel
    lexical: ResponseOverallDataModel
    grammar: ResponseOverallDataModel
    pronunciation: ResponseOverallDataModel