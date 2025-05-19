# MARK: Import 
# Dependency
import re
import datetime
import torch
import numpy as np
from transformers import (
    AutoTokenizer, 
    AutoModelForTokenClassification,
)

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvServerException
from app.utils.rounded_ielts_band import EvRoundedIELTSBand
from app.models.evaluation_model import EvEvaluationModel
from app.utils.logger import ev_logger

# MARK: FluencyService
class FluencyService:
    '''
    FluencyService class is responsible for evaluating the fluency of the speech.
    It uses pre-trained models to detect filled pauses, explicit editing terms,
    discourse markers, coordinating conjunctions, and restart words.
    The class provides methods to download the models, check their availability,
    evaluate the speech rate, long pauses, and token classification.
    It also provides a method to score the fluency based on the evaluation results
    then return the final IELTS band score and feedback.
    '''
    # MARK: Properties
    def __init__(self):
        '''
        Initializes the FluencyService with the given parameters.
        '''
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
        '''
        Start download the model from Hugging Face.
        '''
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
        '''
        Get the model from Hugging Face based on the model name and key model.
        '''
        try:
            ev_logger.info(f'Starting download {model_name} ...')

            # Get the tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name, token = EvIELTSConfig.hugging_face_api_key)

            # Get the model
            model = AutoModelForTokenClassification.from_pretrained(model_name, token = EvIELTSConfig.hugging_face_api_key)

            ev_logger.info(f'Successfully download {model_name} √')

            # Update the model based on key model
            if key_model == 'filled_pauses_model':
                # Update the filled pauses model and tokenizer
                self.filled_pauses_model = model
                self.filled_pauses_tokenizer = tokenizer

                ev_logger.info(f'Successfully update {model_name} √')
            elif key_model == 'explicit_editing_terms_model':
                # Update the explicit editing terms model and tokenizer
                self.explicit_editing_terms_model = model
                self.explicit_editing_terms_tokenizer = tokenizer

                ev_logger.info(f'Successfully update {model_name} √')
            elif key_model == 'discourse_markers_model':
                # Update the discourse markers model and tokenizer
                self.discourse_markers_model = model
                self.discourse_markers_tokenizer = tokenizer

                ev_logger.info(f'Successfully update {model_name} √')
            elif key_model == 'coordinating_conjunctions_model':
                # Update the coordinating conjunctions model and tokenizer
                self.coordinating_conjunctions_model = model
                self.coordinating_conjunctions_tokenizer = tokenizer

                ev_logger.info(f'Successfully update {model_name} √')
            elif key_model == 'restart_words_model':
                # Update restart words model and tokenizer
                self.restart_words_model = model
                self.restart_words_tokenizer = tokenizer

                ev_logger.info(f'Successfully update {model_name} √')
        except Exception as error:
          ev_logger.info(f'Failed to download {model_name} x')
          ev_logger.info(f'Error: {error}')

    # MARK: CheckModel
    def check_model(self):
        '''
        Check if the model and tokenizer are ready.
        '''
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
        '''
        Check the health of the model and tokenizer by returning the status and information of each model and tokenizer.
        '''
        return {
            'filled_pauses_model_ready': self.filled_pauses_model is not None and self.filled_pauses_tokenizer is not None,
            'filled_pauses_model_name': self.filled_pauses_model_name,
            'filled_pauses_base_model': 'BERT',
            'filled_pauses_model_type': 'AutoModelForTokenClassification',
            'filled_pauses_tokenizer_type': 'AutoTokenizer',
            'filled_pauses_model_description': 'Detect filled pauses (e.g. Uh, Um, Mm, Hm)',
            'explicit_editing_terms_model_ready': self.explicit_editing_terms_model is not None and self.explicit_editing_terms_tokenizer is not None,
            'explicit_editing_terms_model_name': self.explicit_editing_terms_model_name,
            'explicit_editing_terms_base_model': 'BERT',
            'explicit_editing_terms_model_type': 'AutoModelForTokenClassification',
            'explicit_editing_terms_tokenizer_type': 'AutoTokenizer',
            'explicit_editing_terms_model_description': 'Detect explicit editing term (e.g. I mean, Sorry)',
            'discourse_markers_model_ready': self.discourse_markers_model is not None and self.discourse_markers_tokenizer is not None,
            'discourse_markers_model_name': self.discourse_markers_model_name,
            'discourse_markers_base_model': 'BERT',
            'discourse_markers_model_type': 'AutoModelForTokenClassification',
            'discourse_markers_tokenizer_type': 'AutoTokenizer',
            'discourse_markers_model_description': 'Detect discourse markers (e.g. You know, Well)',
            'coordinating_conjunctions_model_ready': self.coordinating_conjunctions_model is not None and self.coordinating_conjunctions_tokenizer is not None,
            'coordinating_conjunctions_model_name': self.coordinating_conjunctions_model_name,
            'coordinating_conjunctions_base_model': 'BERT',
            'coordinating_conjunctions_model_type': 'AutoModelForTokenClassification',
            'coordinating_conjunctions_tokenizer_type': 'AutoTokenizer',
            'coordinating_conjunctions_model_description': 'Detect coordinating conjunctions (e.g. And, Or, But)',
            'restart_words_model_ready': self.restart_words_model is not None and self.restart_words_tokenizer is not None,
            'restart_words_model_name': self.restart_words_model_name,
            'restart_words_base_model': 'BERT',
            'restart_words_model_type': 'AutoModelForTokenClassification',
            'restart_words_tokenizer_type': 'AutoTokenizer',
            'restart_words_model_description': 'Detect restart words (e.g. I I mean, Yeh Yes)',
            'timestamp': datetime.datetime.now()
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
        '''
        Update the model based on the parameters.
        '''
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
        '''
        Get the word per minutes based on the total duration and total words.
        '''
        # Get the word per minutes
        return total_words / ((total_duration if total_duration > 0 else 0) / 60)

    # MARK: GetLongPauses
    def _get_long_pauses(self, words: list) -> list:
        '''
        Get the long pauses based on the words list.
        '''
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
        '''
        Get the prediction of the token classification model.
        '''
        try:
            # Tokenize the split input text
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
            ev_logger.info(f'Failed to predict token classification x')

            # If something went wrong
            raise EvServerException(
                f'Failed to predict token classification model: {model}',
                information = {
                    'error': str(error)
                }
            )

    # MARK: GetTimestampFromTokenClassification
    def _get_timestamp_from_token_classification(self, word_asr: list, word_level_predictions: list) -> list:
        '''
        Function to get the timestamp from the token classification.
        '''
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
                        # Remove the space in the word detect
                        word_detect = re.sub(r'\s+([,.!?])\s+', r'\1 ', word_detect)

                        # Add the timestamp
                        timestamp.append((word_detect.strip(), (star_detect, end_detect)))

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
                    # Check if the word detect is not empty
                    if len(word_detect) > 0:
                        # Add space to the word detect
                        word_detect += ' '

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
                    # Check if the word detect is not empty
                    if len(word_detect) > 0:
                        # Add space to the word detect
                        word_detect += ' '

                    # Reset the pointer
                    pointer_asr += 1
                    char_pointer_asr = 0

        # Check if still have the flag label
        if len(word_detect) > 0:
            # Remove the space in the word detect
            word_detect = re.sub(r'\s+([,.!?])\s+', r'\1 ', word_detect)

            # Add the timestamp
            timestamp.append((word_detect.strip(), (star_detect, end_detect)))

        # Return the timestamp based on the token classification
        return timestamp
    
    # MARK: MatchTokensToSpans
    def _match_tokens_to_spans(self, transcription, tokens):
        '''
        Function to match the tokens to the spans in the transcription.
        '''
        # Initialize the list of spans
        spans = []

        # Initialize the pointer
        ptr = 0

        # Loop through the tokens
        for token in tokens:
            # Get the token lower case
            token_lower = token.lower()
            # Skip whitespace
            while ptr < len(transcription) and transcription[ptr].isspace():
                ptr += 1

            # Look for token match
            match_start = ptr

            # Check if the token is in the transcription
            match_end = match_start + len(token)

            while transcription[match_start:match_end].lower() != token_lower and match_end <= len(transcription):
                
                match_start += 1
                match_end = match_start + len(token)
            if match_end <= len(transcription):
                spans.append((match_start, match_end))
                ptr = match_end
            else:
                # Fallback if can't find exact match
                spans.append((ptr, ptr + len(token)))
                ptr += len(token)
        return spans
    
    # MARK: CombineSpansAndLabels
    def _combine_spans_and_labels(self, transcription, token_label_lists):
        '''
        Function to combine the spans and labels.
        '''
        # Initialize the char_labels list with zeros
        char_labels = [0] * len(transcription)

        # Loop through the token label lists
        for token_label_list in token_label_lists:
            # Get the tokens and labels
            tokens, labels = zip(*token_label_list)

            # Get the spans from the tokens
            spans = self._match_tokens_to_spans(transcription, tokens)
            for (start, end), label in zip(spans, labels):
                if label == 1:
                    for i in range(start, end):
                        if i < len(char_labels):
                            char_labels[i] = 1
        return char_labels
    
    # MARK: BuildHighlightedHtml
    def _build_highlighted_html(self, transcription, char_labels):
        output = ""
        i = 0
        while i < len(transcription):
            if char_labels[i] == 1:
                output += '<span style="color:red">'
                while i < len(transcription) and char_labels[i] == 1:
                    output += transcription[i]
                    i += 1
                output += '</span>'
            else:
                output += transcription[i]
                i += 1

        return f'<p><strong>Original Sentence:</strong></p><p>{output}</p>'

    # MARK: EvaluateSpeechRate
    def _evaluate_speech_rate(self, word_per_minutes: float) -> float:
        '''
        Evaluate the speech rate based on the word per minutes.
        '''
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

    # MARK: EvaluateLongPauses
    def _evaluate_long_pauses(self, long_pauses_count: int) -> float:
        '''
        Evaluate the long pauses based on the long pauses count.
        '''
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
        '''
        Evaluate the token classification based on the token classification list.
        '''
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

    # MARK: DetectLinkingWordsNLTK
    def _detect_linking_words_nltk(self, words: list) -> list[str]:
        """
        Detect potential linking words in a given text using NLTK's POS tagging.
        Tags considered: 
        - CC  = Coordinating conjunction (e.g., and, but)
        - IN  = Subordinating conjunction/preposition (e.g., because, although)
        - RB  = Adverb (used for discourse markers like however, therefore)
        """
        linking_candidates = [word['tag'] for word in words if word['tag'] in {"CC", "IN", "RB"}]
        return linking_candidates

    # MARK: EvaluateFluency
    def evaluate_fluency(self, transcribe: str, words: list) -> EvEvaluationModel:
        '''
        Evaluates the fluency of the speech based on the transcribe and words list.
        It calculates the speech rate, long pauses, filled pauses, explicit editing terms,
        discourse markers, coordinating conjunctions, and restart words.
        It returns the final IELTS band score and feedback.
        '''
        try:
            # If the transcribe is empty or words is empty
            if transcribe == '' or not transcribe or len(words) == 0 or not words: 
                # Return ielts band 0
                return EvEvaluationModel(
                    ielts_band = 0,
                    readable_feedback = f'''
                        <p><strong>Feedback:</strong></p>
                        <p>Your transcription is empty. Please provide a valid transcription.</p>
                    ''',
                    feedback_information = {
                        'total_words': 0,
                        'total_duration': 0,
                        'speech_rate': 0,
                        'speech_rate_ielts_band': 0,
                        'long_pauses': [],
                        'long_pauses_ielts_band': 0,
                        'filled_paused_predict': [],
                        'filled_paused_timestamp': [],
                        'filled_paused_ielts_band': 0,
                        'explicit_editing_terms_predict': [],
                        'explicit_editing_terms_timestamp': [],
                        'explicit_editing_terms_ielts_band': 0,
                        'discourse_markers_predict': [],
                        'discourse_markers_timestamp': [],
                        'discourse_markers_ielts_band': 0,
                        'coordinating_conjunctions_predict': [],
                        'coordinating_conjunctions_timestamp': [],
                        'coordinating_conjunctions_ielts_band': 0,
                        'restart_words_predict': [],
                        'restart_words_timestamp': [],
                        'restart_words_ielts_band': 0,
                        'char_label': [],
                    }
                )

            # Calculate total words
            total_words = len(transcribe.split())

            # Calculate total duration
            total_duration = np.float64(words[-1]['end']) - np.float64(words[0]['start']) if len(words) > 1 else np.float64(words[0]['end']) - np.float64(words[0]['start'])

            # Score the speech rate
            speech_rate = self._get_word_per_minutes(total_duration, total_words)

            # Evaluate the speech rate
            speech_rate_ielts_band = self._evaluate_speech_rate(speech_rate)

            # Get the long pauses list
            long_pauses = self._get_long_pauses(words)

            # Evaluate the long pauses
            long_pauses_ielts_band = self._evaluate_long_pauses(len(long_pauses))

            # Check if the words count is more than 2
            if len(words) > 1:
                # Get the first duration of the words
                first_duration = np.float64(words[0]['start'])

                # Check if the first duration is less than 0
                if first_duration < 0:
                    # Set the first duration to 0
                    first_duration = 0

                # Revise long pauses
                if first_duration > 0.5:
                    long_pauses_ielts_band -= 0.5
                elif first_duration > 1:
                    long_pauses_ielts_band -= 1
                elif first_duration > 1.5:
                    long_pauses_ielts_band -= 1.5
                elif first_duration > 2:
                    long_pauses_ielts_band -= 2

                # Make sure long pauses ielts band is between 0 and 9
                long_pauses_ielts_band = max(0, min(long_pauses_ielts_band, 9))

            # Predict the filled paused
            filled_paused_predict = self._get_predict_token_classification(
                text = transcribe, 
                model = self.filled_pauses_model, 
                tokenizer = self.filled_pauses_tokenizer,
            )

            # Get the timestamp from the filled paused
            filled_paused_timestamp = self._get_timestamp_from_token_classification(words, filled_paused_predict)

            # Evaluate the filled paused
            filled_paused_ielts_band = self._evaluate_token_classification(filled_paused_timestamp)

            # Predict explicit editing terms
            explicit_editing_terms_predict = self._get_predict_token_classification(
                text = transcribe, 
                model = self.explicit_editing_terms_model, 
                tokenizer = self.explicit_editing_terms_tokenizer,
            )

            # Get the timestamp from the explicit editing terms
            explicit_editing_terms_timestamp = self._get_timestamp_from_token_classification(words, explicit_editing_terms_predict)

            # Evaluate the explicit editing terms
            explicit_editing_terms_ielts_band = self._evaluate_token_classification(explicit_editing_terms_timestamp)

            # Predict discourse markers
            discourse_markers_predict = self._get_predict_token_classification(
                text = transcribe, 
                model = self.discourse_markers_model, 
                tokenizer = self.discourse_markers_tokenizer,
            )

            # Get the timestamp from the discourse markers
            discourse_markers_timestamp = self._get_timestamp_from_token_classification(words, discourse_markers_predict)
            # Evaluate the discourse markers
            discourse_markers_ielts_band = self._evaluate_token_classification(discourse_markers_timestamp)

            # Predict coordinating conjunctions
            coordinating_conjunctions_predict = self._get_predict_token_classification(
                text = transcribe, 
                model = self.coordinating_conjunctions_model, 
                tokenizer = self.coordinating_conjunctions_tokenizer,
            )

            # Get the timestamp from the coordinating conjunctions
            coordinating_conjunctions_timestamp = self._get_timestamp_from_token_classification(words, coordinating_conjunctions_predict)

            # Evaluate the coordinating conjunctions
            coordinating_conjunctions_ielts_band = self._evaluate_token_classification(coordinating_conjunctions_timestamp)

            # Predict restart words
            restart_words_predict = self._get_predict_token_classification(
                text = transcribe, 
                model = self.restart_words_model, 
                tokenizer = self.restart_words_tokenizer,
            )

            # Get the timestamp from the restart words
            restart_words_timestamp = self._get_timestamp_from_token_classification(words, restart_words_predict)

            # Evaluate the restart words
            restart_words_ielts_band = self._evaluate_token_classification(restart_words_timestamp)

            # Get the word count of the transcribe
            word_count = len(transcribe.split())

            # Get the linking words
            linking_words = self._detect_linking_words_nltk(words)
            linking_present = len(linking_words) > 0

            # Get the labeled words based on the token classification
            char_label = self._combine_spans_and_labels(
                transcribe, 
                [filled_paused_predict, explicit_editing_terms_predict, discourse_markers_predict, restart_words_predict]
            )

            # Get the original sentence feedback
            html_original_sentence = self._build_highlighted_html(transcribe, char_label)

            # Define html correction feedback
            html_correction_feedback = ''

            # Check if in the char label have 1 value
            if 1 in char_label:
                # Check if have filled paused timestamp
                if len(filled_paused_timestamp) > 0:
                    # Aff filled paused timestamp title
                    html_correction_feedback += '<p><strong>Filled Pauses:</strong></p>'
                    
                    # Add ul tag
                    html_correction_feedback += '<ul>'

                    # Loop through the filled paused timestamp
                    for word, timestamp in filled_paused_timestamp:
                        # Add li tag
                        html_correction_feedback += f'<li><span style="color:red">{word}</span> in ({timestamp[0]}s - {timestamp[1]}s)</li>'

                    # Add ul tag
                    html_correction_feedback += '</ul>'

                # Check if have explicit editing terms timestamp
                if len(explicit_editing_terms_timestamp) > 0:
                    # Aff explicit editing terms timestamp title
                    html_correction_feedback += '<p><strong>Explicit Editing Terms:</strong></p>'
                    
                    # Add ul tag
                    html_correction_feedback += '<ul>'

                    # Loop through the explicit editing terms timestamp
                    for word, timestamp in explicit_editing_terms_timestamp:
                        # Add li tag
                        html_correction_feedback += f'<li><span style="color:red">{word}</span> in ({timestamp[0]}s - {timestamp[1]}s)</li>'

                    # Add ul tag
                    html_correction_feedback += '</ul>'

                # Check if have discourse markers timestamp
                if len(discourse_markers_timestamp) > 0:
                    # Aff discourse markers timestamp title
                    html_correction_feedback += '<p><strong>Discourse Markers:</strong></p>'
                    
                    # Add ul tag
                    html_correction_feedback += '<ul>'

                    # Loop through the discourse markers timestamp
                    for word, timestamp in discourse_markers_timestamp:
                        # Add li tag
                        html_correction_feedback += f'<li><span style="color:red">{word}</span> in ({timestamp[0]}s - {timestamp[1]}s)</li>'

                    # Add ul tag
                    html_correction_feedback += '</ul>'

                # Check if have restart words timestamp
                if len(restart_words_timestamp) > 0:
                    # Aff restart words timestamp title
                    html_correction_feedback += '<p><strong>Restart Words:</strong></p>'
                    
                    # Add ul tag
                    html_correction_feedback += '<ul>'

                    # Loop through the restart words timestamp
                    for word, timestamp in restart_words_timestamp:
                        # Add li tag
                        html_correction_feedback += f'<li><span style="color:red">{word}</span> in ({timestamp[0]}s - {timestamp[1]}s)</li>'

                    # Add ul tag
                    html_correction_feedback += '</ul>'

            # Check if the html correction feedback is not empty
            if html_correction_feedback != '':
                # Add the feedback
                html_correction_feedback = f'<p><strong>Correction:</strong></p>{html_correction_feedback}'

            # Define html feedback
            html_feedback = ''

            # Evaluate the word count and linking words
            if word_count < 8:
                # Add the feedback
                html_feedback += 'Your sentence is too short. Try to make it longer. '
            elif word_count < 12:
                # Add the feedback
                html_feedback += 'Your sentence is short. Try to make it longer. '
            elif word_count < 18:
                # Add the feedback
                html_feedback += 'Your response could be more developed. Add linking ideas or more elaboration. '

            # Evaluate the linking words
            if word_count > 12 and not linking_present:
                # Add the feedback
                html_feedback += 'Try using linking words (e.g., because, so, however) to improve coherence. '

            # Evaluate the long pauses
            if len(long_pauses) > 0:
                # Add the long pauses title
                html_feedback += f'You have {len(long_pauses)} long pauses, in '
                
                # Loop through the list
                for index, (start, end) in enumerate(long_pauses):
                    # Add the time stamp in the feedback
                    html_feedback += f'{start} to {end}'

                    # Check if this feedback is last
                    if index < len(long_pauses) - 1:
                        # Add the comma in the feedback
                        html_feedback += ', '
                    else:
                        # Add the dot in the feedback
                        html_feedback += '. '

                # Check the count of the long pauses
                if len(long_pauses) < 2:
                    # Add the feedback
                    html_feedback += 'This is a normal sign of fluency.'
                elif len(long_pauses) < 4:
                    # Add the feedback
                    html_feedback += 'This is a fair sign of fluency.'
                elif len(long_pauses) < 6:
                    # Add the feedback
                    html_feedback += 'This is a poor sign of fluency.'
                else:
                    # Add the feedback
                    html_feedback += 'This is a very poor sign of fluency.'

            # Count the disfluency factors
            disfluency_factors = len(filled_paused_timestamp) + len(explicit_editing_terms_timestamp) + len(discourse_markers_timestamp) + len(coordinating_conjunctions_timestamp) + len(restart_words_timestamp)

            # Evaluate disfluency factors
            if disfluency_factors > 0 and disfluency_factors < 2:
                # Add the feedback
                html_feedback += 'You have a few disfluency factors, which is a normal sign of fluency.'
            elif disfluency_factors < 4:
                # Add the feedback
                html_feedback += 'You have some disfluency factors, which is a fair sign of fluency. Try to reduce them.'
            elif disfluency_factors < 6:
                # Add the feedback
                html_feedback += 'You have many disfluency factors, which is a poor sign of fluency. Do not use them too much.'
            else:
                # Add the feedback
                html_feedback += 'You have a lot of disfluency factors, which is a very poor sign of fluency and should be avoided. Keep practicing to reduce them.'

            # Check if the feedback not empty
            if html_feedback != '':
                # Add the feedback
                html_feedback = f'<p><strong>Feedback:</strong></p><p>{html_feedback}</p>'

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

            # Revise the fluency score
            if word_count < 8:
                fluency_score = min(fluency_score, 5)
            elif word_count < 12:
                fluency_score = min(fluency_score, 6.0 if linking_present else 5.5)
            elif word_count < 18:
                fluency_score = min(fluency_score, 6.5 if linking_present else 6.0)

            # Revise the fluency score
            if word_count > 18 and not linking_present:
                fluency_score -= 0.5
            elif word_count > 18 and linking_present and len(linking_words) < 10:
                fluency_score += 0.5
            elif word_count > 18 and linking_present and len(linking_words) >= 10:
                fluency_score += 1

            # Make sure the fluency score is between 0 and 9
            fluency_score = max(0, min(fluency_score, 9))

            # Rounded to ielts band
            final_ielts_band = EvRoundedIELTSBand(fluency_score).rounded_band

            # Return the evaluation model
            return EvEvaluationModel(
                ielts_band = final_ielts_band,
                readable_feedback = f'<div>{html_original_sentence}{html_correction_feedback}{html_feedback}</div>',
                feedback_information = {
                    'total_words': total_words,
                    'total_duration': total_duration,
                    'speech_rate': speech_rate,
                    'speech_rate_ielts_band': speech_rate_ielts_band,
                    'long_pauses': long_pauses,
                    'long_pauses_ielts_band': long_pauses_ielts_band,
                    'filled_paused_predict': filled_paused_predict,
                    'filled_paused_timestamp': filled_paused_timestamp,
                    'filled_paused_ielts_band': filled_paused_ielts_band,
                    'explicit_editing_terms_predict': explicit_editing_terms_predict,
                    'explicit_editing_terms_timestamp': explicit_editing_terms_timestamp,
                    'explicit_editing_terms_ielts_band': explicit_editing_terms_ielts_band,
                    'discourse_markers_predict': discourse_markers_predict,
                    'discourse_markers_timestamp': discourse_markers_timestamp,
                    'discourse_markers_ielts_band': discourse_markers_ielts_band,
                    'coordinating_conjunctions_predict': coordinating_conjunctions_predict,
                    'coordinating_conjunctions_timestamp': coordinating_conjunctions_timestamp,
                    'coordinating_conjunctions_ielts_band': coordinating_conjunctions_ielts_band,
                    'restart_words_predict': restart_words_predict,
                    'restart_words_timestamp': restart_words_timestamp,
                    'restart_words_ielts_band': restart_words_ielts_band,
                    'char_label': char_label,
                }
            )
        
        except EvServerException as error:
            # Raise the exception
            raise error
        
        except Exception as error:
            # Define the error message
            message = f'Error evaluating fluency: {str(error)}'

            # Raise an exception with the error message
            raise EvServerException(
                message = message,
                information = {
                    'message': message,
                }
            )
    
# MARK: FluencyServiceInstance
# Create the fluency service instance
fluency_service = FluencyService()