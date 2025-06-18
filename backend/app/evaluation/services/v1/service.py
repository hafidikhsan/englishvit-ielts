# MARK: Import
# Dependencies.
import logging
import os
import requests
from fastapi import File, Form, Header, UploadFile
from openai import OpenAI
from typing import Any, Optional

# Modules.
from app.evaluation.models.exception import (
    EvaluationException,
    EvaluationErrorException,
    EvaluationClientException,
    EvaluationServerException,
)
from app.evaluation.models.response import (
    ResponseSingleModel,
    ResponseOverallModel,
)
from config import EvIELTSConfig

# MARK: Variables
# Define some constants for evaluation services.
_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
_single_prompt_dir = os.path.join(_base_dir, "public", "text", "evaluation_feedback.txt")
_overall_prompt_dir = os.path.join(_base_dir, "public", "text", "overall_feedback.txt")

# MARK: PrivateFunctions
# Function to get the prompt from a file.
def _get_prompt(file_path: str) -> str:
    """
    Retrieves the content of a file and returns it as a string.

    Args:
        file_path (str): The path to the file containing the prompt.

    Returns:
        str: The content of the file as a string.
    """
    try:
        # Check if the file not exists.
        if not os.path.exists(file_path):
            # Log the error for debugging purposes.
            logging.error(f"Prompt file {file_path} does not exist.")

            # Raise an exception with a detailed message.
            raise EvaluationErrorException(
                information="Prompt file not found",
                detail=f"The prompt file at {file_path} does not exist."
            )
        
        # Open the file and read its content.
        with open(file_path, "r", encoding="utf-8") as file:
            # Read and return the content of the file.
            return file.read()
        
    except EvaluationException as error:
        # Re-raise the EvaluationException for further handling.
        raise error

    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Error reading prompt file {file_path}: {error}")

        # Raise an EvaluationErrorException with the error details.
        raise EvaluationErrorException(
            information=f"Failed to read prompt file {file_path}",
            detail=str(error)
        )
    
# MARK: GetSingleEvaluation
# Function to get the single evaluation feedback.
async def get_single_evaluation(
    authorization: Optional[str] = Header(None),
    test_id: Optional[Any] = Form(None),
    question: Optional[str] = Form(None),
    answer: Optional[str] = Form(None),
) -> dict:
    """
    Gets the single evaluation feedback based on the provided question and answer.

    Args:
        authorization (Optional[str]): The authorization header for the request.
        test_id (Optional[Any]): An optional test identifier for tracking.
        question (Optional[str]): The question associated with the evaluation.
        answer (Optional[str]): The answer provided for the evaluation.

    Returns:
        dict: A dictionary containing the evaluation feedback.
    """
    # Check if `question` and `answer` are provided.
    if not question or not answer:
        # Log the error for debugging purposes.
        logging.error("Question and answer must be provided for single evaluation.")

        # Raise an EvaluationClientException with a detailed message.
        raise EvaluationClientException(
            information="GET -> Single Evaluation",
            detail="Both question and answer must be provided."
        )
    
    try:
        # Get the single prompt.
        single_prompt = _get_prompt(_single_prompt_dir)

        # Define the OpenAI Whisper client.
        openai_client = OpenAI(
            api_key=EvIELTSConfig.openai_api_key
        )

        # Create the response using the OpenAI chat model.
        response = openai_client.responses.parse(
            model=EvIELTSConfig.openai_chat_model_name,
            instructions=single_prompt,
            input=f"Interviewer question is '{question}' and candidate answer is '{answer}'",
            text_format=ResponseSingleModel,
        )
        
        # Parse the response data.
        response_data = response.output_parsed

        # Check if the response data is valid.
        if not isinstance(response_data, ResponseSingleModel):
            # Log the error for debugging purposes.
            logging.error("Invalid response data format received from OpenAI API.")

            # Raise an EvaluationServerException with a detailed message.
            raise EvaluationServerException(
                information="GET -> Single Evaluation",
                detail="The response data format is invalid."
            )

        # Check if the authorization header is provided.
        if authorization:
            # Check if the test ID is not provided.
            if test_id is None:
                # Log the error for debugging purposes.
                logging.error("Test ID must be provided for saving the evaluation result.")

                # Raise an EvaluationClientException with a detailed message.
                raise EvaluationClientException(
                    information="GET -> Single Evaluation",
                    detail="The test ID must be provided to save the evaluation result."
                )

            # Define headers for the request.
            headers = {
                "Authorization": authorization,
            }

            # Define the data
            data = {
                "finished": 1,
                "fluency_feedback": response_data.fluency.json(),
                "pronunciation_feedback": response_data.pronunciation.json(),
                "grammar_feedback": response_data.grammar.json(),
                "lexical_feedback": response_data.lexical.json(),
            }

            # Send the request to the Englishvit API
            response = requests.post(
                f"https://englishvit.com/api/user/ielts-ai/test/update/{test_id}",
                data=data,
                headers=headers,
            )

            # Check if the response is not successful
            if response.status_code != 200:
                # Log the error for debugging purposes.
                logging.error(f"Failed to update test with ID {test_id}. Status code: {response.status_code}")

                # Raise an EvaluationServerException with a detailed message.
                raise EvaluationServerException(
                    information="GET -> Single Evaluation",
                    detail=f"Failed to update test with ID {test_id}. Status code: {response.status_code}"
                )
            
        # Return the response data as a dictionary.
        return response_data.dict()

    except EvaluationException as error:
        # Re-raise the EvaluationException for further handling.
        raise error
    
    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Error getting single evaluation: {error}")

        # Raise an EvaluationErrorException with the error details.
        raise EvaluationErrorException(
            information="GET -> Single Evaluation",
            detail=str(error)
        )
    
# MARK: GetOverallEvaluation
# Function to get the overall evaluation feedback.
async def get_overall_evaluation(
    authorization: Optional[str] = Header(None),
    session_id: Optional[Any] = Form(None),
    finished: Optional[Any] = Form(None),
    histories: Optional[str] = Form(None),
) -> dict:
    """
    Gets the overall evaluation feedback based on the provided session ID and histories.

    Args:
        authorization (Optional[str]): The authorization header for the request.
        session_id (Optional[Any]): An optional session identifier for tracking.
        finished (Optional[Any]): An optional flag indicating if the evaluation is finished.
        histories (Optional[str]): An optional string containing the evaluation histories.

    Returns:
        dict: A dictionary containing the overall evaluation feedback.
    """
    # Check if `histories` and `finished` are provided.
    if not histories or not finished:
        # Log the error for debugging purposes.
        logging.error("Histories and finished status must be provided for overall evaluation.")

        # Raise an EvaluationClientException with a detailed message.
        raise EvaluationClientException(
            information="GET -> Overall Evaluation",
            detail="The histories and finished status must be provided."
        )
    
    try:
        # Get the overall prompt.
        overall_prompt = _get_prompt(_overall_prompt_dir)

        # Define the OpenAI Whisper client.
        openai_client = OpenAI(
            api_key=EvIELTSConfig.openai_api_key
        )

        # Create the response using the OpenAI chat model.
        response = openai_client.responses.parse(
            model=EvIELTSConfig.openai_chat_model_name,
            instructions=overall_prompt,
            input=f"Candidate histories: {histories}",
            text_format=ResponseOverallModel,
        )
        
        # Parse the response data.
        response_data = response.output_parsed

        # Check if the response data is valid.
        if not isinstance(response_data, ResponseOverallModel):
            # Log the error for debugging purposes.
            logging.error("Invalid response data format received from OpenAI API.")

            # Raise an EvaluationServerException with a detailed message.
            raise EvaluationServerException(
                information="GET -> Overall Evaluation",
                detail="The response data format is invalid."
            )

        # Check if the authorization header is provided.
        if authorization:
            # Check if the session ID is not provided.
            if session_id is None:
                # Log the error for debugging purposes.
                logging.error("Session ID must be provided for saving the evaluation result.")

                # Raise an EvaluationClientException with a detailed message.
                raise EvaluationClientException(
                    information="GET -> Overall Evaluation",
                    detail="The session ID must be provided to save the evaluation result."
                )

            # Define headers for the request.
            headers = {
                "Authorization": authorization
            }

            # Define the data
            data = {
                "finished": finished,
                "overall_band": response_data.overall.final_band,
                "overall_feedback": response_data.overall.model_dump_json(),
                "fluency_band": response_data.fluency.final_band,
                "fluency_feedback": response_data.fluency.model_dump_json(),
                "lexical_band": response_data.lexical.final_band,
                "lexical_feedback": response_data.lexical.model_dump_json(),
                "grammar_band": response_data.grammar.final_band,
                "grammar_feedback": response_data.grammar.model_dump_json(),
                "pronunciation_band": response_data.pronunciation.final_band,
                "pronunciation_feedback": response_data.pronunciation.model_dump_json(),
            }

            # Send the request to the Englishvit API
            response = requests.post(
                f"https://englishvit.com/api/user/ielts-ai/session/update/{session_id}",
                data=data,
                headers=headers,
            )
            # Check if the response is not successful
            if response.status_code != 200:
                # Log the error for debugging purposes.
                logging.error(f"Failed to update session with ID {session_id}. Status code: {response.status_code}")

                # Raise an EvaluationServerException with a detailed message.
                raise EvaluationServerException(
                    information="GET -> Overall Evaluation",
                    detail=f"Failed to update session with ID {session_id}. Status code: {response.status_code}"
                )
            
        # Return the response data as a dictionary.
        return response_data.dict()
    
    except EvaluationException as error:
        # Re-raise the EvaluationException for further handling.
        raise error
    
    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Error getting overall evaluation: {error}")

        # Raise an EvaluationErrorException with the error details.
        raise EvaluationErrorException(
            information="GET -> Overall Evaluation",
            detail=str(error)
        )

# MARK: GetServiceInfo
# Function to get the evaluation service information.
async def get_service_info() -> dict:
    """
    Gets the evaluation service information.

    Returns:
        dict: A dictionary containing the evaluation service information.
    """
    try:
        # Get the single prompt.
        single_prompt = _get_prompt(_single_prompt_dir)

        # Get the overall prompt.
        overall_prompt = _get_prompt(_overall_prompt_dir)

        # Return the evaluation service information.
        return {
            "single_prompt": single_prompt,
            "overall_prompt": overall_prompt,
            "openai_chat_model_name": EvIELTSConfig.openai_chat_model_name,
        }
    
    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Error getting service info: {error}")

        # Raise an EvaluationErrorException with the error details.
        raise EvaluationErrorException(
            information="GET -> Service Info",
            detail=str(error)
        )
    

# MARK: UpdateOpenAIChatModelName
# Function to update the OpenAI chat model name.
async def update_openai_chat_model_name(
    model_name: Optional[str] = Form(None)
) -> dict:
    """
    Updates the OpenAI chat model name.

    Args:
        model_name (Optional[str]): The new OpenAI chat model name to set.

    Returns:
        dict: A dictionary containing the updated OpenAI chat model name.
    """
    try:
        # Check if the model name is provided.
        if not model_name:
            # Log the error for debugging purposes.
            logging.error("No OpenAI chat model name provided.")

            # Raise an EvaluationClientException with a detailed message.
            raise EvaluationClientException(
                information="UPDATE -> OpenAI Chat Model Name",
                detail="The OpenAI chat model name must be provided."
            )
        
        # Update the OpenAI chat model name in the configuration.
        EvIELTSConfig.openai_chat_model_name = model_name

        # Return the updated OpenAI chat model name.
        return {
            "model_name": EvIELTSConfig.openai_chat_model_name
        }
    
    except EvaluationException as error:
        # Re-raise the EvaluationException for further handling.
        raise error
    
    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Error updating OpenAI chat model name: {error}")

        # Raise an EvaluationErrorException with the error details.
        raise EvaluationErrorException(
            information="UPDATE -> OpenAI Chat Model Name",
            detail=str(error)
        )

# MARK: UpdateSinglePrompt
# Function to update the single prompt data.
async def update_single_prompt(
    file: Optional[UploadFile] = File(None),
) -> dict:
    """
    Updates the single prompt data.

    Args:
        file (Optional[UploadFile]): The new single prompt file to set.

    Returns:
        dict: A dictionary containing the updated single prompt.
    """
    # Check if the file is provided.
    if not file:
        # Log the error for debugging purposes.
        logging.error("No single prompt file provided.")

        # Raise an EvaluationClientException with a detailed message.
        raise EvaluationClientException(
            information="UPDATE -> Single Prompt",
            detail="The single prompt file must be provided."
        )
    
    try:
        # Define allowed file types for the single prompt.
        allowed_file_types = ["txt"]

        # Check if the file type is allowed.
        if not file.filename.split(".")[-1].lower() in allowed_file_types:
            # Log the error for debugging purposes.
            logging.error(f"Invalid file type for single prompt: {file.filename}")

            # Raise an EvaluationClientException with a detailed message.
            raise EvaluationClientException(
                information="UPDATE -> Single Prompt",
                detail=f"The file type {file.filename.split('.')[-1]} is not allowed. Allowed types: {', '.join(allowed_file_types)}."
            )
        
        # Read the content of the file.
        content = await file.read()

        # Write the content to the single prompt file.
        with open(_single_prompt_dir, "w", encoding="utf-8") as f:
            f.write(content.decode("utf-8"))

        # Get the single prompt.
        single_prompt = _get_prompt(_single_prompt_dir)

        # Return the updated single prompt.
        return {
            "single_prompt": single_prompt
        }
    
    except EvaluationException as error:
        # Re-raise the EvaluationException for further handling.
        raise error

    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Error updating single prompt: {error}")

        # Raise an EvaluationErrorException with the error details.
        raise EvaluationErrorException(
            information="UPDATE -> Single Prompt",
            detail=str(error)
        )
    
# MARK: UpdateOverallPrompt
async def update_overall_prompt(
    file: Optional[UploadFile] = File(None),
) -> dict:
    """
    Updates the overall prompt data.

    Args:
        file (Optional[UploadFile]): The new overall prompt file to set.

    Returns:
        dict: A dictionary containing the updated overall prompt.
    """
    # Check if the file is provided.
    if not file:
        # Log the error for debugging purposes.
        logging.error("No overall prompt file provided.")

        # Raise an EvaluationClientException with a detailed message.
        raise EvaluationClientException(
            information="UPDATE -> Overall Prompt",
            detail="The overall prompt file must be provided."
        )
    
    try:
        # Define allowed file types for the overall prompt.
        allowed_file_types = ["txt"]

        # Check if the file type is allowed.
        if not file.filename.split(".")[-1].lower() in allowed_file_types:
            # Log the error for debugging purposes.
            logging.error(f"Invalid file type for overall prompt: {file.filename}")

            # Raise an EvaluationClientException with a detailed message.
            raise EvaluationClientException(
                information="UPDATE -> Overall Prompt",
                detail=f"The file type {file.filename.split('.')[-1]} is not allowed. Allowed types: {', '.join(allowed_file_types)}."
            )
        
        # Read the content of the file.
        content = await file.read()

        # Write the content to the overall prompt file.
        with open(_overall_prompt_dir, "w", encoding="utf-8") as f:
            f.write(content.decode("utf-8"))

        # Get the overall prompt.
        overall_prompt = _get_prompt(_overall_prompt_dir)

        # Return the updated overall prompt.
        return {
            "overall_prompt": overall_prompt
        }
    
    except EvaluationException as error:
        # Re-raise the EvaluationException for further handling.
        raise error

    except Exception as error:
        # Log the unexpected error for debugging purposes.
        logging.error(f"Error updating overall prompt: {error}")

        # Raise an EvaluationErrorException with the error details.
        raise EvaluationErrorException(
            information="UPDATE -> Overall Prompt",
            detail=str(error)
        )