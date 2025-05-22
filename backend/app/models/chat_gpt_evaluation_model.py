# MARK: Import
# Dependency
from pydantic import BaseModel

# Modules
from app.models.chat_gpt_evaluation_data_model import EvChatGPTEvaluationDataModel

# MARK: EvChatGPTEvaluationModel
class EvChatGPTEvaluationModel(BaseModel):
    # Properties
    fluency: EvChatGPTEvaluationDataModel
    lexical: EvChatGPTEvaluationDataModel
    grammar: EvChatGPTEvaluationDataModel
    pronunciation: EvChatGPTEvaluationDataModel