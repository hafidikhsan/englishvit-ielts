# MARK: Import
# Dependencies
import datetime
import whisper

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvException, EvClientException, EvServerException, EvAPIException
from app.utils.logger import ev_logger

# MARK: EvASRService
class EvASRService:
    # MARK: Properties
    def __init__(self):
        # Properties
        self.model_name = EvIELTSConfig.whisper_model
        self.model = None
        self.initial_prompt = "I was like, was like, I'm like, you know what I mean, kind of, um, ah, huh, and so, so um, uh, and um, like um, so like, like it's, it's like, i mean, yeah, ok so, uh so, so uh, yeah so, you know, it's uh, uh and, and uh, like, kind"

        # Start download the model
        self._start_download_model(model_name = self.model_name)

    # MARK: StartDownloadModel
    def _start_download_model(self, model_name: str):
        try:
            ev_logger.info(f"Starting download 'Whisper {model_name}' ...")

            # Try to load the ASR model (Whisper)
            self.model = whisper.load_model(model_name)

            ev_logger.info(f"Successfully download 'Whisper {model_name}' √")
        except Exception as error:
            ev_logger.info(f"Failed to download 'Whisper {model_name}' x")
            ev_logger.info(f"Error: {error}")

    # MARK: CheckModel
    def check_model(self):
        return self.model is not None

    # MARK: HealthCheck
    def health_check(self):
        return {
            "model_ready": self.check_model(),
            "model_name": self.model_name,
            "model_type": "Whisper",
            "model_initial_prompt": self.initial_prompt,
            "timestamp": datetime.datetime.now()
        }

    # MARK: UpdateModel
    def update_model(self, model_name: str):
        try:
            # Define available whisper models
            available_models = ["tiny", "tiny.en", "base", "base.en", "small", "small.en", "medium", "medium.en", "large", "turbo"]

            # Check if model name is one of the available models
            if (available_models.count(model_name) == 0):
                raise EvClientException(
                    message = "Invalid model name",
                )

            # Update the model name propertied
            self.model_name = model_name

            # Start download new model
            self._start_download_model(model_name = model_name)

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            print(f"Failed to update model to '{model_name}' currently use '{self.model_name}' x")

            # If something went wrong
            raise EvAPIException(
                message = "Failed to update model",
            )

    # MARK: UpdateInitialPrompt
    def update_initial_prompt(self, initial_prompt: str):
        # Update initial prompt
        self.initial_prompt = initial_prompt

        print(f"Successfully update initial prompt to '{initial_prompt}' √")

    # MARK: Transcribe
    def transcribe(self, audio_file_path: str):
        try:
            # If the model is empty
            if self.model is None:
                raise EvServerException(
                    message = f"Failed transcribe '{self.model_name}' because model is empty",
                )

            # Transcribe the audio
            result = self.model.transcribe(
                audio_file_path,
                language = "en",
                word_timestamps = True,
                initial_prompt = self.initial_prompt,
                fp16 = False,
            )

            # Return the transcribe and the words timestamp
            return result

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            print(f"Failed to transcribe audio '{audio_file_path}' x")

            # If something went wrong
            raise EvAPIException(
                message = f"Failed to transcribe audio '{audio_file_path}'",
            )
        
        
# MARK: EvASRServiceInstance
# Define ASR service instance
asr_service = EvASRService()