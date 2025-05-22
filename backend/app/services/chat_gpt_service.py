# MARK: Import
# Dependencies
import datetime
from openai import OpenAI

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvException, EvAPIException
from app.models.chat_gpt_evaluation_model import EvChatGPTEvaluationModel
from app.models.chat_gpt_overall_evaluation_model import EvChatGPTOverallEvaluationModel
from app.utils.logger import ev_logger

# MARK: EvChatGPTService
class EvChatGPTService:
    # MARK: Properties
    def __init__(self):
        # Properties
        self.model_name = EvIELTSConfig.chatgpt_model
        self.fluency_prompt = """
        First evaluation metrics is Fluency and Coherence, and evaluate the candidate's response based on these criteria:
        - Relevance to the question
        - Overall coherence
        - Abrupt transitions
        - Logical sequencing of ideas
        - Use of discourse markers (e.g., so, well, however)
        - Filled pauses (e.g., um, uh)
        - Repetition or restarts
        - Use of coordinating conjunctions (e.g., and, but, or)
        - Explicit editing terms (e.g., I mean, sorry)
        """
        self.lexical_prompt = """
        Second evaluation metrics is Lexical Resource, and evaluate the candidate's response based on these criteria:
        - Relevance to the question
        - Range of vocabulary (everyday + topic-specific)
        - Use of collocations and idiomatic expressions
        - Accuracy of word choice and word forms
        - Paraphrasing and avoidance of repetition
        - Appropriateness and naturalness of language
        - CEFR-level vocabulary analysis
        """
        self.grammar_prompt = """
        Third evaluation metrics is Grammatical Range and Accuracy, and evaluate the candidate's response based on these criteria:
        - Relevance to the question
        - Range of sentence structures (simple, compound, complex)
        - Grammatical features (modal verbs, passive, conditionals, relative clauses)
        - Verb tense/aspect accuracy and variety
        - Subject-verb agreement and article usage
        - Number and type of grammar errors
        """
        self.pronunciation_prompt = """
        Last evaluation metrics is Pronunciation, and evaluate the candidate's response based on these criteria:
        - Relevance to the question
        - Mispronunciations that led to incorrect or unusual transcriptions (e.g., "liberry" → "library")
        - Incomplete or broken words
        - Unusual spelling that may indicate slurred or unclear speech
        - Homophones or confusion between similar-sounding words
        - Intelligibility and rhythm (e.g., unnatural sentence fragments)
        """

    # MARK: HealthCheck
    def health_check(self):
        return {
            "model_name": self.model_name,
            "model_type": "ChatGPT",
            "fluency_prompt": self.fluency_prompt,
            "lexical_prompt": self.lexical_prompt,
            "grammar_prompt": self.grammar_prompt,
            "pronunciation_prompt": self.pronunciation_prompt,
            "timestamp": datetime.datetime.now()
        }

    # MARK: UpdateModel
    def update_model(self, model_name: str):
        # Update model name
        self.model_name = model_name

        ev_logger.info(f"Successfully update model to '{self.model_name}' √")


    # MARK: UpdatePrompt
    def update_prompt(
        self, 
        fluency_prompt: str = None,
        lexical_prompt: str = None,
        grammar_prompt: str = None,
        pronunciation_prompt: str = None,
    ):
        # Update prompt
        self.fluency_prompt = fluency_prompt if fluency_prompt is not None else self.fluency_prompt
        self.lexical_prompt = lexical_prompt if lexical_prompt is not None else self.lexical_prompt
        self.grammar_prompt = grammar_prompt if grammar_prompt is not None else self.grammar_prompt
        self.pronunciation_prompt = pronunciation_prompt if pronunciation_prompt is not None else self.pronunciation_prompt

        ev_logger.info(f"Successfully update prompt √")

    # MARK: GetPrompt
    def get_prompt(self):
        # Get prompt
        return {
            "fluency_prompt": self.fluency_prompt,
            "lexical_prompt": self.lexical_prompt,
            "grammar_prompt": self.grammar_prompt,
            "pronunciation_prompt": self.pronunciation_prompt,
        }

    # MARK: Evaluate
    def evaluate(self, question: str, answer: str) -> EvChatGPTEvaluationModel:
        try:
            # Define Client
            client = OpenAI(
              api_key = EvIELTSConfig.openai_api_key,
            )
            # Define Prompt
            system_prompt = f"""
            You are an IELTS Speaking examiner expert that have attention to the detail and precision, evaluate candidate answer based on the question for each evaluation metrics. 

            {self.fluency_prompt}

            {self.lexical_prompt}

            {self.grammar_prompt}

            {self.pronunciation_prompt}

            Provide feedback for each evaluation metrics with
            - Final IELTS band score from 0.0 to 9.0 (Don't forget use based on IELTS band rules like 6.5, 7.0, 7.5 don't use 6.1, 6.2, 6.3)
            - 'feedback' 2-7 sentences, highlighting key words with <strong> if needed and wrapped with <p> HTML tag.
            - Bullet point like 2 or 7 sentences, highlighting key words with <strong> if needed and wrapped with <p> HTML tag.
            - Make the 'feedback' short and motivating, written in a style that's friendly for Gen Z learners.
            - Use a conversational tone (like you're giving advice to a peer).
            - Use emojis to make it fun and encouraging (e.g., 🔥, 💡, ✨, 🚀).
            - Don't write same information in 'feedback' and 'points'.
            - You can mention user answer in the 'feedback' or 'points' (like 'Yo still have 'uh' in your answer') if needed.
            """

            # Evaluate process
            result = client.responses.parse(
                model = self.model_name,
                instructions = system_prompt,
                input = f"Interviewer question is '{question}' and candidate answer is '{answer}'",
                text_format = EvChatGPTEvaluationModel,
            )

            # Return model
            return result.output_parsed

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            ev_logger.info(f"Failed to evaluate for '{question}' and candidate answer is '{answer}' x")

            # If something went wrong
            raise EvAPIException(
                message = f"Failed to evaluate for '{question}' and candidate answer is '{answer}' x",
            )
        
    # MARK: OverallFeedback
    def overall_feedback(self, histories: str) -> EvChatGPTOverallEvaluationModel:
        try:
            # Define Client
            client = OpenAI(
              api_key = EvIELTSConfig.openai_api_key,
            )
            # Define Prompt
            system_prompt = f"""
            You are an IELTS Speaking examiner expert that have attention to the detail and precision, evaluate overall IELTS speaking simulation of this candidate based on speaking simulation history.

            Provide feedback for each evaluation metrics  and the overall with
            - Final IELTS band score from 0.0 to 9.0 (Don't forget use based on IELTS band rules like 6.5, 7.0, 7.5 don't use 6.1, 6.2, 6.3)
            - 'readable_feedback' with 2-7 sentences, highlighting key words with <strong> if needed and wrapped with <p> HTML tag.
            - Make the 'readable_feedback' short and motivating, written in a style that's friendly for Gen Z learners.
            - Use a conversational tone (like you're giving advice to a peer).
            - Use emojis to make it fun and encouraging (e.g., 🔥, 💡, ✨, 🚀).
            """

            # Evaluate process
            result = client.responses.parse(
                model = self.model_name,
                instructions = system_prompt,
                input = f"Here is the candidate's speaking simulation history: {histories}",
                text_format = EvChatGPTOverallEvaluationModel,
            )

            # Return model
            return result.output_parsed

        except EvException as error:
            # If the error is EvException
            raise error

        except Exception as error:
            ev_logger.info(f"Failed to overall feedback x")

            # If something went wrong
            raise EvAPIException(
                message = f"Failed to overall feedback for x",
            )
        
# MARK: EvChatGPTServiceInstance
# Define ChatGPT service instance
chatgpt_service = EvChatGPTService()