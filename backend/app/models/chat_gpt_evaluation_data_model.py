# MARK: Import
# Dependency
from pydantic import BaseModel

# Modules
from app.models.chat_gpt_evaluation_feedback_model import EvChatGPTEvaluationFeedbackModel

# MARK: EvChatGPTEvaluationDataModel
class EvChatGPTEvaluationDataModel(BaseModel):
    # Properties
    final_band: float
    readable_feedback: EvChatGPTEvaluationFeedbackModel