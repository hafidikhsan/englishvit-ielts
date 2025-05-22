# MARK: Import
# Dependency
from pydantic import BaseModel

# MARK: EvChatGPTOverallEvaluationFeedbackModel
class EvChatGPTOverallEvaluationFeedbackModel(BaseModel):
    # Properties
    final_band: float
    readable_feedback: str