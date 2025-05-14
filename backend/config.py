# MARK: Import
# Dependencies
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MARK: EvIELTSConfig
class EvIELTSConfig:
    # MARK: Flask
    flask_app = os.getenv('FLASK_APP')
    flask_env = os.getenv('FLASK_ENV', 'production')
    flask_debug = os.getenv('FLASK_DEBUG', 0) == 1
    flask_run_port = os.getenv('FLASK_RUN_PORT', 5000)

    # MARK: Audio
    audio_clean_extension = os.getenv('AUDIO_CLEAN_EXTENSION')
    audio_clean_sample_rate = int(os.getenv('AUDIO_CLEAN_SAMPLE_RATE'))
    audio_clean_channels = int(os.getenv('AUDIO_CLEAN_CHANNELS'))
    
    # MARK: ML Model
    hugging_face_api_key = os.getenv('HUGGING_FACE_API_KEY')
    asr_model_name = os.getenv('ASR_MODEL_NAME')
    spacy_model_name = os.getenv('SPACY_MODEL_NAME')
    fluency_filled_pauses_model_name = os.getenv('FLUENCY_FILLED_PAUSES')
    fluency_explicit_editing_terms_model_name = os.getenv('FLUENCY_EXPLICIT_EDITING_TERMS')
    fluency_discourse_markers_model_name = os.getenv('FLUENCY_DISCOURSE_MAKERS')
    fluency_coordinating_conjunction_model_name = os.getenv('FLUENCY_COORDINATING_CONJUNCTION')
    fluency_restart_words_model_name = os.getenv('FLUENCY_RESTART_WORDS')
    lexical_cefr_classification_model_name = os.getenv('LEXICAL_CEFR_CLASSIFICATION_MODEL_NAME')
    lexical_bert_fill_masked_model_name = os.getenv('LEXICAL_BERT_FILL_MASKED_MODEL_NAME')
    lexical_bert_fill_masked_model_task = os.getenv('LEXICAL_BERT_FILL_MASKED_MODEL_TASK')
    grammar_grammarly_gec_model_name = os.getenv('GRAMMAR_GRAMMARLY_GEC_MODEL_NAME')
    grammar_happy_gec_base_model_name = os.getenv('GRAMMAR_HAPPY_GEC_BASE_MODEL_NAME')
    grammar_happy_gec_model_name = os.getenv('GRAMMAR_HAPPY_GEC_MODEL_NAME')
    grammar_open_source_gec_model_name = os.getenv('GRAMMAR_OPEN_SOURCE_GEC_MODEL_NAME')
    grammar_open_source_gec_model_task = os.getenv('GRAMMAR_OPEN_SOURCE_GEC_MODEL_TASK')
    tokenizer_max_length = int(os.getenv('TOKENIZER_MAX_LENGTH'))
    long_pauses_threshold = float(os.getenv('LONG_PAUSE_THRESHOLD'))

    # MARK: Logging
    log_level = os.getenv('LOG_LEVEL')

    # MARK: Application
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')