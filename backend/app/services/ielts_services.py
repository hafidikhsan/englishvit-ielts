# MARK: Import
# Dependencies
import os
import json
import datetime
from openai import OpenAI
from flask import current_app
from silero_vad import load_silero_vad, read_audio, get_speech_timestamps

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvException, EvAPIException, EvServerException
from app.models.chat_gpt_evaluation_model import EvChatGPTEvaluationModel
from app.models.chat_gpt_overall_evaluation_model import EvChatGPTOverallEvaluationModel
from app.models.evaluation_model import EvEvaluationModel
from app.models.response_transcribe_model import EvResponseTranscribeModel
from app.utils.logger import ev_logger

# Get the JSON directory
def get_json_dir():
    return os.path.abspath(os.path.join(current_app.root_path, "..", "json_data"))

# MARK: EvIELTSService
class EvIELTSService:
    # MARK: Properties
    def __init__(self):
        # Properties
        self.chatgpt_feedback_model_name = EvIELTSConfig.chatgpt_feedback_model
        self.chatgpt_whisper_model_name = EvIELTSConfig.chatgpt_whisper_model
        self.silero_model = None
        self.user_credit = 2
        self.evaluation_feedback_prompt = ""
        self.overall_feedback_prompt = ""
        self.initial_prompt = "I was like, was like, I'm like, you know what I mean, kind of, um, ah, huh, and so, so um, uh, and um, like um, so like, like it's, it's like, i mean, yeah, ok so, uh so, so uh, yeah so, you know, it's uh, uh and, and uh, like, kind"

        # Get prompt
        self._get_feedback_prompt()

    # MARK: GetFeedbackPrompt
    def _get_feedback_prompt(self):
        try:
            # Define path
            json_dir = get_json_dir()
            evaluation_path = os.path.join(json_dir, EvIELTSConfig.evaluation_feedback_prompt)
            overall_path = os.path.join(json_dir, EvIELTSConfig.overall_feedback_prompt)
            self.silero_model = load_silero_vad()

            # Read evaluation feedback prompt
            with open(evaluation_path, 'r', encoding='utf-8') as file:
                self.evaluation_feedback_prompt = file.read()

            # Read overall feedback prompt
            with open(overall_path, 'r', encoding='utf-8') as file:
                self.overall_feedback_prompt = file.read()

            ev_logger.info(f"Successfully update prompt √")

        except Exception as error:
            ev_logger.info(f"Failed to update prompt x")


    # MARK: HealthCheck
    def health_check(self):
        return {
            "chatgpt_feedback_model_name": self.chatgpt_feedback_model_name,
            "chatgpt_whisper_model_name": self.chatgpt_whisper_model_name,
            "evaluation_feedback_prompt": self.evaluation_feedback_prompt,
            "overall_feedback_prompt": self.overall_feedback_prompt,
            "initial_prompt": self.initial_prompt,
            "timestamp": datetime.datetime.now()
        }

    # MARK: UpdateModel
    def update_model(
        self, 
        chatgpt_feedback_model_name: str = None, 
        chatgpt_whisper_model_name: str = None,
    ):
        # Update model name
        self.chatgpt_feedback_model_name = chatgpt_feedback_model_name if chatgpt_feedback_model_name is not None else self.chatgpt_feedback_model_name
        self.chatgpt_whisper_model_name = chatgpt_whisper_model_name if chatgpt_whisper_model_name is not None else self.chatgpt_whisper_model_name

        ev_logger.info(f"Successfully update model to '{self.model_name}' √")


    # MARK: UpdatePrompt
    def update_prompt(self):
        # Update prompt
        self._get_feedback_prompt()

    # MARK: UpdateInitialPrompt
    def update_initial_prompt(self, initial_prompt: str):
        # Update initial prompt
        self.initial_prompt = initial_prompt

        ev_logger.info(f"Successfully update initial prompt to '{initial_prompt}' √")

    # MARK: UpdateCredit
    def update_credit(self, user_credit: int):
        # Update user credit
        self.user_credit = user_credit

        ev_logger.info(f"Successfully update user credit to '{self.user_credit}' √")

    # MARK: GetCredit
    def get_credit(self) -> int:
        # Get user credit
        return self.user_credit

    # MARK: GetPrompt
    def get_prompt(self):
        # Get prompt
        return {
            "evaluation_feedback_prompt": self.evaluation_feedback_prompt,
            "overall_feedback_prompt": self.overall_feedback_prompt,
            "initial_prompt": self.initial_prompt,
        }

    # MARK: Evaluate
    def evaluate(self, audio_file_path: str, question: str) -> EvEvaluationModel:
        try:
            # If the feedback model is empty
            if self.chatgpt_feedback_model_name is None:
                raise EvServerException(
                    message = f"Failed evaluate because feedback model is empty",
                )
            else:
                if self.chatgpt_feedback_model_name == "":
                    raise EvServerException(
                        message = f"Failed evaluate because feedback model is empty",
                    )

            # If the whisper model is empty
            if self.chatgpt_whisper_model_name is None:
                raise EvServerException(
                    message = f"Failed evaluate because whisper model is empty",
                )
            else:
                if self.chatgpt_whisper_model_name == "":
                    raise EvServerException(
                        message = f"Failed evaluate because whisper model is empty",
                    )

            # If the evaluation prompt is empty
            if self.evaluation_feedback_prompt is None:
                raise EvServerException(
                    message = f"Failed evaluate because evaluation prompt is empty",
                )
            else:
                if self.evaluation_feedback_prompt == "":
                    raise EvServerException(
                        message = f"Failed evaluate because evaluation prompt is empty",
                    )

            # Define Chat GPT client
            client = OpenAI(
                api_key = EvIELTSConfig.openai_api_key,
            )

            # Open audio file
            audio_file = open(audio_file_path, "rb")

            # Transcribe
            transcript = client.audio.transcriptions.create(
              file = audio_file,
              model = self.chatgpt_whisper_model_name,
              language = "en",
              prompt = self.initial_prompt,
              response_format = "verbose_json",
              temperature = 0.0,
              timestamp_granularities = ["word"],
            )

            # Get transcribe text
            transcript_text = transcript.text

            # Get word timestamps
            word_timestamps = []
            for word in transcript.words:
                word_timestamps.append({
                    "word": word.word,
                    "start": word.start,
                    "end": word.end,
                })

            # Evaluate process
            result = client.responses.parse(
                model = self.chatgpt_feedback_model_name,
                instructions = self.evaluation_feedback_prompt,
                input = f"Interviewer question is '{question}' and candidate answer is '{transcript_text}'",
                text_format = EvChatGPTEvaluationModel,
            )

            # Return evaluation data
            return EvEvaluationModel(
                evaluation = result.output_parsed,
                transcript = transcript_text,
                word_timestamp = json.dumps(word_timestamps),
            )

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            ev_logger.info(f"Failed to evaluate '{audio_file_path}' x")

            # If something went wrong
            raise EvAPIException(
                message = f"Failed to evaluate '{audio_file_path}'",
            )

    # MARK: OverallFeedback
    def overall_feedback(self, histories: str) -> EvChatGPTOverallEvaluationModel:
        try:
            # If the feedback model is empty
            if self.chatgpt_feedback_model_name is None:
                raise EvServerException(
                    message = f"Failed evaluate because feedback model is empty",
                )
            else:
                if self.chatgpt_feedback_model_name == "":
                    raise EvServerException(
                        message = f"Failed evaluate because feedback model is empty",
                    )

            # If the overall prompt is empty
            if self.overall_feedback_prompt is None:
                raise EvServerException(
                    message = f"Failed evaluate because overall prompt is empty",
                )
            else:
                if self.overall_feedback_prompt == "":
                    raise EvServerException(
                        message = f"Failed evaluate because overall prompt is empty",
                    )

            # Define Chat GPT client
            client = OpenAI(
                api_key = EvIELTSConfig.openai_api_key,
            )

            # Evaluate process
            result = client.responses.parse(
                model = self.chatgpt_feedback_model_name,
                instructions = self.overall_feedback_prompt,
                input = f"Here is the candidate's speaking simulation history: {histories}",
                text_format = EvChatGPTOverallEvaluationModel,
            )

            # Return evaluation data
            return result.output_parsed

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            ev_logger.info(f"Failed to overall feedback x")

            # If something went wrong
            raise EvAPIException(
                message = f"Failed to overall feedback",
            )

    # MARK: Transcribe
    def transcribe(self, audio_file_path: str) -> EvResponseTranscribeModel:
        try:
            # If the whisper model is empty
            if self.chatgpt_whisper_model_name is None or self.silero_model is None:
                raise EvServerException(
                    message = f"Failed evaluate because whisper and silero model is empty",
                )
            else:
                if self.chatgpt_whisper_model_name == "":
                    raise EvServerException(
                        message = f"Failed evaluate because whisper model is empty",
                    )

            # Define Chat GPT client
            client = OpenAI(
                api_key = EvIELTSConfig.openai_api_key,
            )

            # VAD process
            wav = read_audio(audio_file_path)
            speech_timestamps = get_speech_timestamps(
                wav,
                self.silero_model,
                return_seconds=True,
            )

            # If no speech detected
            if not speech_timestamps:
                # Return transcribe data
                return EvResponseTranscribeModel(
                    transcribe = "",
                    word_timestamp = json.dumps([]),
                )
            else:
                # Open audio file
                audio_file = open(audio_file_path, "rb")

                # Transcribe
                transcript = client.audio.transcriptions.create(
                file = audio_file,
                model = self.chatgpt_whisper_model_name,
                language = "en",
                prompt = self.initial_prompt,
                response_format = "verbose_json",
                temperature = 0.0,
                timestamp_granularities = ["word"],
                )

                # Get transcribe text
                transcript_text = transcript.text

                # Get word timestamps
                word_timestamps = []
                for word in transcript.words:
                    word_timestamps.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end,
                    })

                # Return transcribe data
                return EvResponseTranscribeModel(
                    transcribe = transcript_text,
                    word_timestamp = json.dumps(word_timestamps),
                )

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            ev_logger.info(f"Failed to transcribe '{audio_file_path}' x")

            # If something went wrong
            raise EvAPIException(
                message = f"Failed to transcribe '{audio_file_path}'",
            )
        
    # MARK: Evaluation
    def evaluation(self, answer: str, question: str) -> EvChatGPTEvaluationModel:
        try:
            # If the feedback model is empty
            if self.chatgpt_feedback_model_name is None:
                raise EvServerException(
                    message = f"Failed evaluate because feedback model is empty",
                )
            else:
                if self.chatgpt_feedback_model_name == "":
                    raise EvServerException(
                        message = f"Failed evaluate because feedback model is empty",
                    )

            # If the evaluation prompt is empty
            if self.evaluation_feedback_prompt is None:
                raise EvServerException(
                    message = f"Failed evaluate because evaluation prompt is empty",
                )
            else:
                if self.evaluation_feedback_prompt == "":
                    raise EvServerException(
                        message = f"Failed evaluate because evaluation prompt is empty",
                    )

            # Define Chat GPT client
            client = OpenAI(
                api_key = EvIELTSConfig.openai_api_key,
            )

            # Evaluate process
            result = client.responses.parse(
                model = self.chatgpt_feedback_model_name,
                instructions = self.evaluation_feedback_prompt,
                input = f"Interviewer question is '{question}' and candidate answer is '{answer}'",
                text_format = EvChatGPTEvaluationModel,
            )

            # Return evaluation data
            return result.output_parsed

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            ev_logger.info(f"Failed to evaluation x")

            # If something went wrong
            raise EvAPIException(
                message = f"Failed to evaluation",
            )
        
# MARK: EvIELTSServiceInstance
# Define Ev IELTS Service instance
ielts_service = EvIELTSService()