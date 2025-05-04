# Import dependency
import datetime
import torch
import numpy as np
from transformers import (
    AutoTokenizer, 
    AutoModelForTokenClassification,
)

# Import modules
from config import EvIELTSConfig
from app.utils.exception import EvException
from app.utils.rounded_ielts_band import EvRoundedIELTSBand
from app.utils.logger import ev_logger

# MARK: FluencyService
class FluencyService:
    '''
    A class to manage all the fluency IELTS assessment services. This
    class will calculate the fluency score, the IELTS band, feedback.
    '''
    # MARK: Init
    def __init__(self):
        # Class properties
        self.filled_pauses_model_name = EvIELTSConfig.fluency_filled_pauses_model_name
        self.filled_pauses_tokenizer = None
        self.filled_pauses_model = None
        self.explicit_editing_terms_model_name = EvIELTSConfig.fluency_explicit_editing_terms_model_name
        self.explicit_editing_terms_tokenizer = None
        self.explicit_editing_terms_model = None
        self.discourse_markers_model_name = EvIELTSConfig.fluency_discourse_markers_model_name
        self.discourse_markers_tokenizer = None
        self.discourse_markers_model = None
        self.coordinating_conjunctions_model_name = EvIELTSConfig.fluency_coordinating_conjunction_model_name
        self.coordinating_conjunctions_tokenizer = None
        self.coordinating_conjunctions_model = None
        self.restart_words_model_name = EvIELTSConfig.fluency_restart_words_model_name
        self.restart_words_tokenizer = None
        self.restart_words_model = None
        self.tokenizer_max_length = EvIELTSConfig.tokenizer_max_length
        self.long_pause_threshold = EvIELTSConfig.long_pauses_threshold

        # Start download the model
        self._start_download_model(model_names = {
            'filled_pauses_model': self.filled_pauses_model_name,
            'explicit_editing_terms_model': self.explicit_editing_terms_model_name,
            'discourse_markers_model': self.discourse_markers_model_name,
            'coordinating_conjunctions_model': self.coordinating_conjunctions_model_name,
            'restart_words_model': self.restart_words_model_name,
        })

    # MARK: StartDownloadModel
    def _start_download_model(self, model_names: dict):
        ev_logger.info(f'Initiate to start download models ...')

        # Loop through the model names
        for key, value in model_names.items():
            self._get_model(
                key_model = key, 
                model_name = value
            )

        ev_logger.info(f'Finish download models ...')

    # MARK: GetModel
    def _get_model(self, key_model: str, model_name: str):
        try:
            ev_logger.info(f'Starting download {model_name} ...')

            # Get the tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name, token = EvIELTSConfig.hugging_face_api_key)

            # Get the model
            model = AutoModelForTokenClassification.from_pretrained(model_name, token = EvIELTSConfig.hugging_face_api_key)

            ev_logger.info(f'Successfuly download {model_name} √')

            # Update the model based on key model
            if key_model == 'filled_pauses_model':
                # Update the filled pauses model and tokenizer
                self.filled_pauses_model = model
                self.filled_pauses_tokenizer = tokenizer

                ev_logger.info(f'Successfuly update {model_name} √')
            elif key_model == 'explicit_editing_terms_model':
                # Update the explicit editing terms model and tokenizer
                self.explicit_editing_terms_model = model
                self.explicit_editing_terms_tokenizer = tokenizer

                ev_logger.info(f'Successfuly update {model_name} √')
            elif key_model == 'discourse_markers_model':
                # Update the discourse markers model and tokenizer
                self.discourse_markers_model = model
                self.discourse_markers_tokenizer = tokenizer

                ev_logger.info(f'Successfuly update {model_name} √')
            elif key_model == 'coordinating_conjunctions_model':
                # Update the coordinating conjunctions model and tokenizer
                self.coordinating_conjunctions_model = model
                self.coordinating_conjunctions_tokenizer = tokenizer

                ev_logger.info(f'Successfuly update {model_name} √')
            elif key_model == 'restart_words_model':
                # Update restart words model and tokenizer
                self.restart_words_model = model
                self.restart_words_tokenizer = tokenizer

                ev_logger.info(f'Successfuly update {model_name} √')
        except Exception as error:
          ev_logger.info(f'Failed to download {model_name} ×')
          ev_logger.info(f'Error: {error}')

    # MARK: CheckModel
    def check_model(self):
        # Filled pauses model and tokenizer
        filled_pauses_model_ready = self.filled_pauses_model is not None and self.filled_pauses_tokenizer is not None

        # Explicit editing terms model and tokenizer
        explicit_editing_terms_model_ready = self.explicit_editing_terms_model is not None and self.explicit_editing_terms_tokenizer is not None

        # Discourse markers model and tokenizer
        discourse_markers_model_ready = self.discourse_markers_model is not None and self.discourse_markers_tokenizer is not None

        # Coordinating conjunction
        coordinating_conjunctions_model_ready = self.coordinating_conjunctions_model is not None and self.coordinating_conjunctions_tokenizer is not None

        # Restart words model and tokenizer
        restart_words_model_ready = self.restart_words_model is not None and self.restart_words_tokenizer is not None

        # Return the value based on the model and tokenizer condition
        return filled_pauses_model_ready and explicit_editing_terms_model_ready and discourse_markers_model_ready and coordinating_conjunctions_model_ready and restart_words_model_ready

    # MARK: HealthCheck
    def health_check(self):
        return {
            'filled_pauses_model_ready': self.filled_pauses_model is not None and self.filled_pauses_tokenizer is not None,
            'filled_pauses_model_name': self.filled_pauses_model_name,
            'filled_pauses_base_model': 'BERT',
            'filled_pauses_model_type': 'AutoModelForTokenClassification',
            'filled_pauses_tokenizer_type': 'AutoTokenizer',
            'filled_pauses_model_description': 'Detech filled pauses (e.g. Uh, Um, Mm, Hm)',
            'explicit_editing_terms_model_ready': self.explicit_editing_terms_model is not None and self.explicit_editing_terms_tokenizer is not None,
            'explicit_editing_terms_model_name': self.explicit_editing_terms_model_name,
            'explicit_editing_terms_base_model': 'BERT',
            'explicit_editing_terms_model_type': 'AutoModelForTokenClassification',
            'explicit_editing_terms_tokenizer_type': 'AutoTokenizer',
            'explicit_editing_terms_model_description': 'Detech explicit editing term (e.g. I mean, Sorry)',
            'discourse_markers_model_ready': self.discourse_markers_model is not None and self.discourse_markers_tokenizer is not None,
            'discourse_markers_model_name': self.discourse_markers_model_name,
            'discourse_markers_base_model': 'BERT',
            'discourse_markers_model_type': 'AutoModelForTokenClassification',
            'discourse_markers_tokenizer_type': 'AutoTokenizer',
            'discourse_markers_model_description': 'Detech discourse markers (e.g. You know, Well)',
            'coordinating_conjunctions_model_ready': self.coordinating_conjunctions_model is not None and self.coordinating_conjunctions_tokenizer is not None,
            'coordinating_conjunctions_model_name': self.coordinating_conjunctions_model_name,
            'coordinating_conjunctions_base_model': 'BERT',
            'coordinating_conjunctions_model_type': 'AutoModelForTokenClassification',
            'coordinating_conjunctions_tokenizer_type': 'AutoTokenizer',
            'coordinating_conjunctions_model_description': 'Detech coordinating conjunctions (e.g. And, Or, But)',
            'restart_words_model_ready': self.restart_words_model is not None and self.restart_words_tokenizer is not None,
            'restart_words_model_name': self.restart_words_model_name,
            'restart_words_base_model': 'BERT',
            'restart_words_model_type': 'AutoModelForTokenClassification',
            'restart_words_tokenizer_type': 'AutoTokenizer',
            'restart_words_model_description': 'Detech restart words (e.g. I I mean, Yeh Yes)',
            'time_stamp': datetime.datetime.now()
        }

    # MARK: UpdateModel
    def update_model(
        self, 
        filled_pauses_model: str = None,
        explicit_editing_terms_model: str = None,
        discourse_markers_model: str = None,
        coordinating_conjunctions_model: str = None,
        restart_words_model: str = None
    ):
        # Define the dictionary of updated model
        updates_model = dict()

        # Fill the dict based on the parameters
        if filled_pauses_model is not None:
            updates_model['filled_pauses_model'] = filled_pauses_model

        if explicit_editing_terms_model is not None:
            updates_model['explicit_editing_terms_model'] = explicit_editing_terms_model

        if discourse_markers_model is not None:
            updates_model['discourse_markers_model'] = discourse_markers_model

        if coordinating_conjunctions_model is not None:
            updates_model['coordinating_conjunctions_model'] = coordinating_conjunctions_model

        if restart_words_model is not None:
            updates_model['restart_words_model'] = restart_words_model

        # Start download new model
        self._start_download_model(model_names = updates_model)

    # MARK: GetWordPerMinutes
    def _get_word_per_minutes(self, total_duration: float, total_words: float) -> float:
        # Get the word per minutes
        return total_words / ((total_duration if total_duration > 0 else 0) / 60)

    # MARK: GetLongPauses
    def _get_long_pauses(self, words: list) -> list:
        # Check if list is empty return empty list
        if len(words) == 0: return []

        # Define variable to save the timestamp long pauses
        long_pauses = []

        # Define a flag to save the last speech time
        last_speech_time = None

        # Loop through the words
        for word in words:
            # If last speech time is None
            if last_speech_time is None:
                # Set the last speech time
                last_speech_time = word['end']
            else:
                # Get the start duration
                star_word = word['start']

                # Check if the start word is more than last speech time
                if star_word >= last_speech_time:
                    # Calculate the pause duration between 2 word
                    pauses = np.float64(star_word) - np.float64(last_speech_time)

                    # Check if the pauses over the threshold
                    if pauses > self.long_pause_threshold:
                        # Add the long pauses counter
                        long_pauses.append((last_speech_time, star_word))

                    # Update the last speech time
                    last_speech_time = word['end']

        # Return the long pauses timestamp list
        return long_pauses

    # MARK: GetPredictTokenClassification
    def _get_predict_token_classification(self, text: str, model, tokenizer) -> list:
        try:
            # Tokenize the splited input text
            inputs = tokenizer(
                text.split(),
                return_tensors = 'pt',
                truncation = True,
                is_split_into_words = True,
                padding = 'max_length',
                max_length = self.tokenizer_max_length
            )

            # Perform inference
            with torch.no_grad():
                outputs = model(**inputs)
            predictions = outputs.logits.argmax(dim = -1).squeeze().tolist()

            # Decode the predictions
            tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze().tolist())
            word_level_predictions = [
                (token, pred)
                for token, pred in zip(tokens, predictions[:len(tokens)])
                if token not in tokenizer.all_special_tokens
            ]

            # Return the list of token classification
            return word_level_predictions
        except Exception as error:
            ev_logger.info(f'Failed to predict token classification ×')

            # If something went wrong
            raise EvException(
                f'Failed to predict token classification model: {model}',
                status_code = 501,
                information = {
                    'error': str(error)
                }
            )

    # MARK: GetTimestampFromTokenClassification
    def _get_timestamp_from_token_classification(self, word_asr: list, word_level_predictions: list) -> list:
        # Define variable to save the timestamp
        timestamp = []

        # Define variable to store the pointer position
        pointer_asr, pointer_prediction = 0, 0
        char_pointer_asr, char_pointer_prediction = 0, 0

        # A flag to know if the label is in order
        word_detect = ''
        star_detect = None
        end_detect = None

        # Loop until pointer react the length
        while pointer_asr < len(word_asr) and pointer_prediction < len(word_level_predictions):
            # Decode the information
            word_prediction, label_prediction = word_level_predictions[pointer_prediction]
            word_asr_data = word_asr[pointer_asr]
            word_asr_text = word_asr_data['text']
            start_asr = word_asr_data['start']
            end_asr = word_asr_data['end']

            # If the character is match
            if word_asr_text[char_pointer_asr].lower() == word_prediction[char_pointer_prediction].lower():
                # Check if the prediction is true
                if label_prediction == 1:
                    # Add the character to word detect
                    word_detect += word_prediction[char_pointer_prediction].lower()

                    # If the start character
                    if not star_detect:
                        # Add the start time stamp
                        star_detect = start_asr

                    # Add the end time stamp
                    end_detect = end_asr

                # If not the prediction
                else:
                    # If the word length not more than 1
                    if len(word_detect) > 0:
                        # Add the timestamp
                        timestamp.append((word_detect, (star_detect, end_detect)))

                    # Reset the flag label
                    word_detect = ''
                    star_detect = None
                    end_detect = None

                # Add the character pointer
                char_pointer_asr += 1
                char_pointer_prediction += 1

                # If the pointer reach the end of the word predict
                if char_pointer_prediction >= len(word_prediction):
                    # Reset the pointer
                    pointer_prediction += 1
                    char_pointer_prediction = 0

                # If the pointer reach the end of the word asr
                if char_pointer_asr >= len(word_asr_text):
                    # Reset the pointer
                    pointer_asr += 1
                    char_pointer_asr = 0

            else:
                # If the pointer reach the end of the word predict
                if char_pointer_prediction < len(word_prediction):
                    # Reset the pointer
                    pointer_prediction += 1
                    char_pointer_prediction = 0

                # If the pointer reach the end of the word asr
                if char_pointer_asr < len(word_asr_text):
                    # Reset the pointer
                    pointer_asr += 1
                    char_pointer_asr = 0

        # Check if still have the flag label
        if len(word_detect) > 0:
            # Add the timestamp
            timestamp.append((word_detect, (star_detect, end_detect)))

        # Return the timestamp based on the token classification
        return timestamp

    # MARK: EvaluateSpeechRate
    def _evaluate_speech_rate(self, word_per_minutes: float) -> float:
        # Return the IELTS band based on the word per minutes
        if word_per_minutes >= 160: return 9
        elif word_per_minutes >= 140: return 8
        elif word_per_minutes >= 120: return 7
        elif word_per_minutes >= 100: return 6
        elif word_per_minutes >= 90: return 5
        elif word_per_minutes >= 70: return 4
        elif word_per_minutes >= 50: return 3
        elif word_per_minutes >= 30: return 2
        elif word_per_minutes > 0: return 1
        else: return 0

    # EvaluateLongPauses
    def _evaluate_long_pauses(self, long_pauses_count: int) -> float:
        # Return the IELTS band based on long pauses count
        if long_pauses_count < 1: return 9
        elif long_pauses_count < 2: return 8
        elif long_pauses_count < 3: return 7
        elif long_pauses_count < 4: return 6
        elif long_pauses_count < 5: return 5
        elif long_pauses_count < 7: return 4
        elif long_pauses_count < 9: return 3
        elif long_pauses_count < 12: return 2
        elif long_pauses_count < 15: return 1
        else: return 0

    # MARK: EvaluateTokenClassification
    def _evaluate_token_classification(self, token_classification: list) -> float:
        # Get the count of the token classification pauses
        token_classification_words_count = len(token_classification)

        # Return the IELTS band based on token classification words count
        if token_classification_words_count < 1: return 9
        elif token_classification_words_count < 2: return 8
        elif token_classification_words_count < 3: return 7
        elif token_classification_words_count < 4: return 6
        elif token_classification_words_count < 5: return 5
        elif token_classification_words_count < 7: return 4
        elif token_classification_words_count < 9: return 3
        elif token_classification_words_count < 12: return 2
        elif token_classification_words_count < 15: return 1
        else: return 0

    # MARK: Score
    def score(self, transcribe: str, words: list) -> tuple[float, str]:
        # If the transcribe is empty or words is empty
        if transcribe == '' or not transcribe or len(words) == 0 or not words: 
            return (0, 'Not detect a speech.')

        # Define text to save the information evaluation of the dictionary
        feedback = ''

        # Calculate total words
        total_words = len(transcribe.split())

        # Add the total words to the feedback
        feedback += f'Candidate have speech {total_words} words, '

        # Calculate total duration
        total_duration = np.float64(words[-1]['end']) - np.float64(words[0]['start']) if len(words) > 1 else np.float64(words[0]['end']) - np.float64(words[0]['start'])

        # Add the total duration in the feedback
        feedback += f'total duration {total_duration}, '

        # Score the speech rate
        speech_rate = self._get_word_per_minutes(total_duration, total_words)

        # Add the speech rate in the feedback
        feedback += f'get the speech rate {speech_rate} word per minutes, '

        # Evaluate the speech rate
        speech_rate_ielts_band = self._evaluate_speech_rate(speech_rate)

        # Add the speech rate namd in the feedback
        feedback += f'and get final IELTS band based of our system and speech rate is {speech_rate_ielts_band}. '

        # Get the long pauses list
        long_pauses = self._get_long_pauses(words)

        # If have long pauses
        if len(long_pauses) > 0:
            # Add the long pauses counter
            feedback += f'Candidate have {len(long_pauses)} long pauses, with the pauses in '

            # Loop through the list
            for index, (start, end) in enumerate(long_pauses):
                # Add the time stamp in the feedback
                feedback += f'{start} to {end}'

                # Check if this feedback is last
                if index < len(long_pauses) - 1:
                    # Add the comma in the feedback
                    feedback += ', '
                else:
                    # Add the dot in the feedback
                    feedback += '. '

        # Evaluate the long pauses
        long_pauses_ielts_band = self._evaluate_long_pauses(len(long_pauses))

        # Add the long pauses namd in the feedback
        feedback += f'Get final IELTS band based of our system and long pauses count is {long_pauses_ielts_band}. '

        # Predict the filled paused
        filled_paused_predict = self._get_predict_token_classification(
            text = transcribe, 
            model = self.filled_pauses_model, 
            tokenizer = self.filled_pauses_tokenizer,
        )

        # Get the timestamp from the filled paused
        filled_paused_timestamp = self._get_timestamp_from_token_classification(words, filled_paused_predict)

        # Add the filled pauses data to the feedback
        feedback += f'Candidate have {len(filled_paused_timestamp)} filled pauses'

        # Check if have filled pauses
        if len(filled_paused_timestamp) > 0:
            # Add the feedback
            feedback += ', with the pauses in '

            # Loop through the list
            for index, (word, (start, end)) in enumerate(filled_paused_timestamp):
                # Add the time stamp in the feedback
                feedback += f'{start} to {end} with the word [{word}]'

                # Check if this feedback is last
                if index < len(filled_paused_timestamp) - 1:
                    # Add the comma in the feedback
                    feedback += ', '
                else:
                    # Add the dot in the feedback
                    feedback += '. '
        else:
            # Add the feedback
            feedback += '. '

        # Evaluate the filled paused
        filled_paused_ielts_band = self._evaluate_token_classification(filled_paused_timestamp)

        # Add the final filled pauses band in the feedback
        feedback += f'Get final IELTS band based of our system and filled pauses count is {filled_paused_ielts_band}. '

        # Predict explicit editing terms
        explicit_editing_terms_predict = self._get_predict_token_classification(
            text = transcribe, 
            model = self.explicit_editing_terms_model, 
            tokenizer = self.explicit_editing_terms_tokenizer,
        )

        # Get the timestamp from the explicit editing terms
        explicit_editing_terms_timestamp = self._get_timestamp_from_token_classification(words, explicit_editing_terms_predict)

        # Add the explicit editing term data to the feedback
        feedback += f'Candidate have {len(explicit_editing_terms_timestamp)} explicit editing terms'
        
        # Check if have explicit editing terms 
        if len(explicit_editing_terms_timestamp) > 0:
            # Add the feedback
            feedback += ', with the explicit editing terms in '

            # Loop through the list
            for index, (word, (start, end)) in enumerate(explicit_editing_terms_timestamp):
                # Add the time stamp in the feedback
                feedback += f'{start} to {end} with the word [{word}]'

                # Check if this feedback is last
                if index < len(explicit_editing_terms_timestamp) - 1:
                    # Add the comma in the feedback
                    feedback += ', '
                else:
                    # Add the dot in the feedback
                    feedback += '. '
        else:
            # Add the feedback
            feedback += '. '

        # Evaluate the explicit editing terms
        explicit_editing_terms_ielts_band = self._evaluate_token_classification(explicit_editing_terms_timestamp)

        # Add the final explicit editing terms band in the feedback
        feedback += f'Get final IELTS band based of our system and explicit editing terms count is {explicit_editing_terms_ielts_band}. '

        # Predict discourse markers
        discourse_markers_predict = self._get_predict_token_classification(
            text = transcribe, 
            model = self.discourse_markers_model, 
            tokenizer = self.discourse_markers_tokenizer,
        )

        # Get the timestamp from the discourse markers
        discourse_markers_timestamp = self._get_timestamp_from_token_classification(words, discourse_markers_predict)

        # Add the discourse markers data to the feedback
        feedback += f'Candidate have {len(discourse_markers_timestamp)} discourse markers'

        # Check if have discourse markers
        if len(discourse_markers_timestamp) > 0:
            # Add the feedback
            feedback += ', with the discourse markers in '

            # Loop through the list
            for index, (word, (start, end)) in enumerate(discourse_markers_timestamp):
                # Add the time stamp in the feedback
                feedback += f'{start} to {end} with the word [{word}]'

                # Check if this feedback is last
                if index < len(discourse_markers_timestamp) - 1:
                    # Add the comma in the feedback
                    feedback += ', '
                else:
                    # Add the dot in the feedback
                    feedback += '. '
        else:
            # Add the feedback
            feedback += '. '

        # Evaluate the discourse markers
        discourse_markers_ielts_band = self._evaluate_token_classification(discourse_markers_timestamp)

        # Add the final discourse markers band in the feedback
        feedback += f'Get final IELTS band based of our system and discourse markers count is {discourse_markers_ielts_band}. '

        # Predict coordinating conjunctions
        coordinating_conjunctions_predict = self._get_predict_token_classification(
            text = transcribe, 
            model = self.coordinating_conjunctions_model, 
            tokenizer = self.coordinating_conjunctions_tokenizer,
        )

        # Get the timestamp from the coordinating conjunctions
        coordinating_conjunctions_timestamp = self._get_timestamp_from_token_classification(words, coordinating_conjunctions_predict)

        # Add the coordinating conjunctions data to the feedback
        feedback += f'Candidate have {len(coordinating_conjunctions_timestamp)} coordinating conjunctions'

        # Check if have coordinating conjunctions
        if len(coordinating_conjunctions_timestamp) > 0:
            # Add the feedback
            feedback += ', with the coordinating conjunctions in '

            # Loop through the list
            for index, (word, (start, end)) in enumerate(coordinating_conjunctions_timestamp):
                # Add the time stamp in the feedback
                feedback += f'{start} to {end} with the word [{word}]'

                # Check if this feedback is last
                if index < len(coordinating_conjunctions_timestamp) - 1:
                    # Add the comma in the feedback
                    feedback += ', '
                else:
                    # Add the dot in the feedback
                    feedback += '. '
        else:
            # Add the feedback
            feedback += '. '

        # Evaluate the coordinating conjunctions
        coordinating_conjunctions_ielts_band = self._evaluate_token_classification(coordinating_conjunctions_timestamp)

        # Add the final coordinating conjunctions band in the feedback
        feedback += f'Get final IELTS band based of our system and coordinating conjunctions count is {coordinating_conjunctions_ielts_band}. '

        # Predict restart words
        restart_words_predict = self._get_predict_token_classification(
            text = transcribe, 
            model = self.restart_words_model, 
            tokenizer = self.restart_words_tokenizer,
        )

        # Get the timestamp from the restart words
        restart_words_timestamp = self._get_timestamp_from_token_classification(words, restart_words_predict)

        # Add the restart words data to the feedback
        feedback += f'Candidate have {len(restart_words_timestamp)} restart words'

        # Check if have restart words
        if len(restart_words_timestamp) > 0:
            # Add the feedback
            feedback += ', with the restart words in '

            # Loop through the list
            for index, (word, (start, end)) in enumerate(restart_words_timestamp):
                # Add the time stamp in the feedback
                feedback += f'{start} to {end} with the word [{word}]'

                # Check if this feedback is last
                if index < len(restart_words_timestamp) - 1:
                    # Add the comma in the feedback
                    feedback += ', '
                else:
                    # Add the dot in the feedback
                    feedback += '. '
        else:
            # Add the feedback
            feedback += '. '

        # Evaluate the restart words
        restart_words_ielts_band = self._evaluate_token_classification(restart_words_timestamp)

        # Add the final restart words band in the feedback
        feedback += f'Get final IELTS band based of our system and restart words count is {restart_words_ielts_band}. '

        # Weighted average
        fluency_score = (
            (speech_rate_ielts_band * 0.1) +
            (filled_paused_ielts_band * 0.25) +
            (explicit_editing_terms_ielts_band * 0.15) +
            (discourse_markers_ielts_band * 0.15) +
            (coordinating_conjunctions_ielts_band * 0.05) +
            (restart_words_ielts_band * 0.1) +
            (long_pauses_ielts_band * 0.2)
        )

        # Get final fluency band
        fluency_score = EvRoundedIELTSBand(fluency_score).rounded_band

        # Add the final fluency IELTS band
        feedback += f'Get final IELTS band based of our system and fluency score is {fluency_score}.'

        # Return final IELTS fluency criteria and the feedback
        return (fluency_score, feedback)
    
# MARK: FluencyService
# Create the fluency service
fluency_service = FluencyService()