# MARK: Import
# Dependency
from pydantic import BaseModel

# MARK: EvChatGPTEvaluationFeedbackModel
class EvChatGPTEvaluationFeedbackModel(BaseModel):
    # Properties
    feedback: str
    candidate_answer: str
    points: list[str]