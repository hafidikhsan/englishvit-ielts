# MARK: Import
# Dependency
from pydantic import BaseModel

# MARK: EvChatGPTEvaluationFeedbackModel
class EvChatGPTEvaluationFeedbackModel(BaseModel):
    # Properties
    feedback: str
    points: list[str]