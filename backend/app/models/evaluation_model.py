# MARK: Import
# Dependency
from pydantic import BaseModel

# Modules
from app.models.chat_gpt_evaluation_model import EvChatGPTEvaluationModel

# MARK: EvEvaluationModel
class EvEvaluationModel(BaseModel):
    # Properties
    evaluation: EvChatGPTEvaluationModel
    transcript: str
    word_timestamp: str