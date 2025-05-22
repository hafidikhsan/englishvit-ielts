# MARK: Import
# Dependency
from pydantic import BaseModel

# Modules
from app.models.chat_gpt_overall_evaluation_feedback_model import EvChatGPTOverallEvaluationFeedbackModel

# MARK: EvChatGPTOverallEvaluationModel
class EvChatGPTOverallEvaluationModel(BaseModel):
    # Properties
    overall: EvChatGPTOverallEvaluationFeedbackModel
    fluency: EvChatGPTOverallEvaluationFeedbackModel
    lexical: EvChatGPTOverallEvaluationFeedbackModel
    grammar: EvChatGPTOverallEvaluationFeedbackModel
    pronunciation: EvChatGPTOverallEvaluationFeedbackModel