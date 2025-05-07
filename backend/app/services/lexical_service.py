# MARK: Import 
# Dependency
import datetime
import string
import torch
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
from nltk import pos_tag
from lexical_diversity import lex_div as ld
from nltk.tokenize import sent_tokenize, word_tokenize
from wordfreq import tokenize as wordfreq_tokenize, zipf_frequency
from transformers import (
    pipeline,
    AutoTokenizer, 
    AutoModelForSequenceClassification,
)

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvException
from app.services.spacy_service import spacy_service
from app.utils.rounded_ielts_band import EvRoundedIELTSBand
from app.models.evaluation import EvEvaluationModel
from app.utils.logger import ev_logger

# MARK: LexicalService
class LexicalService:
    '''
    LexicalService is a class to manage all the lexical service. In this service will download
    CEFR classification model and bert fill masked model. The CEFR classification model is used to classify
    text to CEFR level and the bert fill masked model is used to fill masked words in sentences.
    The lexical service will also provide a method to evaluate the lexical sophistication, lexical diversity,
    lexical collocation, and repetition words in a transcription. From the evaluation, the lexical service
    will return the IELTS band score and feedback.
    '''
    # MARK: Properties
    def __init__(self):
        '''
        Initializes the LexicalService with the given parameters.
        '''
        self.cefr_classification_model_name = EvIELTSConfig.lexical_cefr_classification_model_name
        self.cefr_classification_model = None
        self.cefr_classification_tokenizer = None
        self.bert_fill_masked_model_name = EvIELTSConfig.lexical_bert_fill_masked_model_name
        self.bert_fill_masked_model_task = EvIELTSConfig.lexical_bert_fill_masked_model_task
        self.bert_fill_masked_model = None
        self.important_tags = {
            'NN', 'NNS', 'NNP', 'NNPS',
            'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
            'JJ', 'JJR', 'JJS',
            'RB', 'RBR', 'RBS',
        }

        # Start download the model
        self._start_download_model()

    # MARK: StartDownloadModel
    def _start_download_model(self):
        '''
        Function to start download the model. This function will download all the model
        that is used in the lexical service. The model that is downloaded are:
        - CEFR classification model
        - BERT fill masked model
        '''
        try:
            ev_logger.info(f'Starting download {self.cefr_classification_model_name} ...')

            # Get the tokenizer
            self.cefr_classification_tokenizer = AutoTokenizer.from_pretrained(
                self.cefr_classification_model_name, 
                token = EvIELTSConfig.hugging_face_api_key
            )

            # Get the model
            self.cefr_classification_model = AutoModelForSequenceClassification.from_pretrained(
                self.cefr_classification_model_name, 
                token = EvIELTSConfig.hugging_face_api_key
            )

            ev_logger.info(f'Successfully download {self.cefr_classification_model_name} √')

            ev_logger.info(f'Starting download {self.bert_fill_masked_model_name} ...')

            # Get the model
            self.bert_fill_masked_model = pipeline(
                self.bert_fill_masked_model_task,
                self.bert_fill_masked_model_name, 
                token = EvIELTSConfig.hugging_face_api_key,
            )

            ev_logger.info(f'Successfully download {self.bert_fill_masked_model_name} √')
        except Exception as error:
          ev_logger.info(f'Failed to download models ×')
          ev_logger.info(f'Error: {error}')

    # MARK: CheckModel
    def check_model(self):
        '''
        Function to check if the model is ready. This function will return True if the model is ready
        '''
        return self.cefr_classification_model is not None and self.cefr_classification_tokenizer is not None and self.bert_fill_masked_model is not None

    # MARK: HealthCheck
    def health_check(self):
        '''
        Function to check the health of the model. This function will return the
        information about the model. 
        '''
        return {
            'cefr_classification_model_ready': self.cefr_classification_model is not None and self.cefr_classification_tokenizer is not None,
            'cefr_classification_model_name': self.cefr_classification_model_name,
            'cefr_classification_base_model': 'BERT',
            'cefr_classification_model_type': 'AutoModelForSequenceClassification',
            'cefr_classification_tokenizer_type': 'AutoTokenizer',
            'cefr_classification_model_description': 'Classify text to CEFR level',
            'bert_fill_masked_model_ready': self.bert_fill_masked_model is not None,
            'bert_fill_masked_model_name': self.bert_fill_masked_model_name,
            'bert_fill_masked_base_model': 'BERT',
            'bert_fill_masked_model_type': self.bert_fill_masked_model_task,
            'bert_fill_masked_model_description': 'Fill masked to predict the next word',
            'time_stamp': datetime.datetime.now()
        }
        
    # MARK: UpdateModel
    def update_model(self):
        '''
        Function to update the model. This function will update the model to the latest
        version.
        '''
        # Start download new model
        self._start_download_model()

    # MARK: GetLexicalSophistication
    def _get_lexical_sophistication(self, words: list) -> dict:
        '''
        Function to get the lexical sophistication of the words. This function will
        categorize the words into 4 categories:
        - Very common
        - Common
        - Less common
        - Advanced
        '''
        # Define level of each data and the empty list to store the words
        levels = {
            'advanced': [],
            'less_common': [],
            'common': [],
            'very_common': []
        }

        # Loop through the words list
        for word in words:
            # Define the lexical sophistication each word
            frequency = zipf_frequency(word, 'en')

            # If the frequency is less than 4, categorize to advance
            if frequency < 4.0:
                levels['advanced'].append(word)

            # If the frequency between 4 and 4.5, categorize to less common
            elif 4.0 <= frequency < 4.5:
                levels['less_common'].append(word)

            # If the frequency between 4.5 and 5, categorize to common
            elif 4.5 <= frequency < 5.0:
                levels['common'].append(word)

            # Else, categorize to very common
            else:
                levels['very_common'].append(word)

        # Return the levels information
        return levels
    
    # MARK: GetContentWords
    def _get_content_words(self, transcribe: str) -> list:
        '''
        Function to get the content words from the transcribe. This function will remove
        the stop words and punctuation from the transcribe. The content words are the
        words that are not stop words and not punctuation. The function will return
        a list of content words.
        '''
        # Get the stop word from nltk
        stop_words = set(stopwords.words('english'))

        # Get the word in the transcribe
        words = transcribe.lower().translate(str.maketrans('', '', string.punctuation)).split()

        # Return a list that contain transcribe words without stop words
        return [word for word in words if word not in stop_words]

    # MARK: GetRepetitionWordsWithoutStopWord
    def _get_repetition_words_without_stop_word(self, transcribe: str) -> dict:
        '''
        Function to get the repetition words without stop word. This function will
        return a dict of the repetition words and the count of the words.
        '''
        # Get the content of the words
        words = self._get_content_words(transcribe)

        # Count each word
        word_counts = Counter(words)

        # Return the dict of the repetition words
        return {word: count for word, count in word_counts.items() if count > 1}
    
    # MARK: GetLexicalCollocationPrediction
    def _get_lexical_collocation_prediction(self, transcribe: str) -> list:
        '''
        Function to get the lexical collocation prediction. This function will
        return a list of the lexical collocation prediction. The prediction will
        contain the word, the sentence, and the prediction result. The prediction
        result will be a list of the predicted words.
        '''
        # Get the stop word from nltk
        stop_words = set(stopwords.words('english'))

        # Tokenize the transcribe
        sentences = sent_tokenize(transcribe)

        # Define variable to store the lexical collocation prediction
        lexical_collocation_prediction = []

        # Loop through the sentences
        for sentence in sentences:
            # Word tokenize the sentence
            word_tokenize_sentence = word_tokenize(sentence)

            # Tagging the sentence
            word_pos_tags = pos_tag(word_tokenize_sentence)

            # Define variable to save the the potential masked and masked predict result
            potential_masked = []

            # Loop through the word pos tags
            for index, (word, tag) in enumerate(word_pos_tags):
                # If tag in the define important tags, word is alpha numeric, and not the stop word
                if tag in self.important_tags and word.isalpha() and word.lower() not in stop_words:
                    potential_masked.append((index, word.lower()))

            # Check if have potential masked data
            if potential_masked:
                # Loop through the masked data
                for masked in potential_masked:
                    # Define the text that have been masked
                    masked_text = ''

                    # Loop through the word post tag
                    for index_pos_tag, (word, tag) in enumerate(word_pos_tags):
                        # If the current post tag equal with potential masked word
                        if index_pos_tag == masked[0]:
                            # Masked the text
                            masked_text += '[MASK] '
                        else:
                            # Add the word
                            masked_text += word + ' '

                    # Doing prediction
                    predictions = self.bert_fill_masked_model(masked_text.strip())

                    # Get the prediction result
                    predicted_words = [pred['token_str'] for pred in predictions]

                    # Add the predict in the lexical collocation predict
                    lexical_collocation_prediction.append((
                        masked[-1] in predicted_words[:5],
                        masked[-1],
                        masked_text.replace('[MASK]', f'[MASK -> {predicted_words[:5]}]'),
                        sentence,
                    ))

        # Return the lexical collocation predictions
        return lexical_collocation_prediction

    # MARK: GetLexicalCollocationScore
    def _get_lexical_collocation_score(self, lexical_collocation_prediction: list) -> float:
        '''
        Function to get the lexical collocation score. This function will return
        a score of the lexical collocation prediction. The score will be calculated
        by dividing the number of correct prediction by the total number of prediction.
        The score will be multiplied by 100 and rounded to 3 decimal places.
        '''
        # If the prediction is empty return 0
        if not lexical_collocation_prediction:
            return 0

        return round((sum([1 for pred in lexical_collocation_prediction if pred[0]]) / len(lexical_collocation_prediction)) * 100, 3)

    # MARK: EvaluateLexicalSophistication
    def _evaluate_lexical_sophistication(self, distribution: dict, repetition_score: float, total_words: float) -> float:
        '''
        Function to evaluate the lexical sophistication. This function will return
        the IELTS band based on the lexical sophistication. The lexical sophistication
        will be calculated based on the distribution of the words. The distribution
        will be categorized into 4 categories:
        - Very common: 0
        - Common: 1
        - Less common: 2
        - Advanced: 3
        '''
        # Calculate the needed data from the distribution
        advance = len(distribution['advanced']) / total_words
        less_common = len(distribution['less_common']) / total_words
        very_common = len(distribution['very_common']) / total_words

        # Mapping into ielts band
        if advance > 0.3 and less_common > 0.2 and repetition_score < 0.15 and very_common < 0.4:
            return 9
        elif advance > 0.2 and less_common > 0.2 and repetition_score < 0.2 and very_common < 0.5:
            return 8
        elif advance > 0.1 and less_common > 0.15 and repetition_score < 0.25 and very_common < 0.6:
            return 7
        elif advance > 0.05 and less_common > 0.1 and repetition_score < 0.3 and very_common < 0.7:
            return 6
        else:
            return 5
        
    # MARK: EvaluateCEFRBandClassification
    def _evaluate_cefr_band_classification(self, transcribe: str) -> float:
        '''
        Function to evaluate the CEFR band classification. This function will return
        the IELTS band based on the CEFR classification. The CEFR classification will
        be done by using the CEFR classification model. The model will classify the input
        text into a CEFR band.
        '''
        # Tokenize the input
        inputs = self.cefr_classification_tokenizer(
            transcribe,
            return_tensors = 'pt'
        )

        # Inference
        with torch.no_grad():
            logits = self.cefr_classification_model(**inputs).logits

        # Predict the cefr band
        predicted_class_id = logits.argmax().item()
        label = self.cefr_classification_model.config.id2label[predicted_class_id]

        # Mapping cefr to ielts
        cefr_to_ielts = {
            'A1': 2,
            'A2': 3,
            'B1': 4,
            'B2': 6,
            'C1': 7.5,
            'C2': 9,
        }

        # Return the IELTS band based on token classification words count
        return EvRoundedIELTSBand(cefr_to_ielts[label]).rounded_band

    # MARK: EvaluateLexicalDiversity
    def _evaluate_lexical_diversity(self, transcribe: str) -> float:
        '''
        Function to evaluate the lexical diversity. This function will return
        the IELTS band based on the lexical diversity. The lexical diversity will
        be calculated based on the MTLD (Measure of Textual Lexical Diversity).
        The MTLD will be calculated based on the tokenized words. The MTLD will
        be calculated using the lexical_diversity library. The MTLD will be
        calculated based on the tokenized words. This function will return
        the IELTS band based on the MTLD score. 
        '''
        # Tokenize the transcribe
        word_token = ld.tokenize(transcribe)

        # Calculate the mltd score
        mtld_score = round(ld.mtld(word_token), 4)

        # Mapping into the ielts score
        if mtld_score > 100:
            return 9
        elif mtld_score > 80:
            return 8
        elif mtld_score > 60:
            return 7
        elif mtld_score > 40:
            return 6
        else:
            return 5

    # MARK: EvaluateRepetitionWordsWithoutStopWord
    def _evaluate_repetition_words_without_stop_word(self, repetition_words: dict) -> float:
        '''
        Function to evaluate the repetition words without stop word. This function will return
        the IELTS band based on the repetition words. The repetition words will be calculated
        based on the repetition words without stop word. 
        '''
        # Calculate the repetition rate
        repetition_rate = round(sum(repetition_words.values()) / len(repetition_words) if len(repetition_words) > 0 else 0, 3)

        # Mapping to ielts band
        if repetition_rate < 0.1:
            return 9
        elif repetition_rate < 0.2:
            return 7
        elif repetition_rate < 0.3:
            return 6
        elif repetition_rate < 0.5:
            return 5
        else:
            return 4

    # MARK: EvaluateLexicalCollocationScore
    def _evaluate_lexical_collocation_score(self, lexical_collocation_score: int) -> float:
        '''
        Function to evaluate the lexical collocation score. This function will return
        the IELTS band based on the lexical collocation score. 
        '''
        # Return the IELTS band based on lexical collocation score
        if lexical_collocation_score >= 100: return 9
        elif lexical_collocation_score >= 95: return 8
        elif lexical_collocation_score >= 85: return 7
        elif lexical_collocation_score >= 75: return 6
        elif lexical_collocation_score >= 60: return 5
        elif lexical_collocation_score >= 45: return 4
        elif lexical_collocation_score >= 30: return 3
        elif lexical_collocation_score >= 15: return 2
        else: return 1

    # MARK: Evaluation
    def evaluate_lexical(self, transcribe: str) -> EvEvaluationModel:
        ''' 
        Evaluates the lexical of the transcribe. The lexical evaluation will be done by using
        prediction model. The prediction model will classify the input text into a CEFR band.
        The model will classify the input text into a CEFR band. The model will also evaluate
        the lexical sophistication, lexical diversity, lexical collocation using fill masked 
        model, and repetition words in the transcription. The model will return the IELTS band 
        score and feedback.
        '''
        try:
            # If the transcribe is empty or words is empty
            if transcribe == '' or not transcribe: 
                # Return ielts band 0
                return EvEvaluationModel(
                    ielts_band = 0,
                    readable_feedback = f'''
                        <p><strong>Feedback:</strong></p>
                        <p>Your transcription is empty. Please provide a valid transcription.</p>
                    ''',
                    feedback_information = {
                        'cefr_classification': [],
                        'lexical_cefr_classification_band': 0,
                        'lexical_sophistication': {},
                        'lexical_sophistication_ielts_band': 0,
                        'lexical_diversity_ielts_band': 0,
                        'repetition_words': {},
                        'repetition_words_ielts_band': 0,
                        'lexical_collocation_prediction': {},
                        'lexical_collocation_score': 0,
                        'lexical_collocation_ielts_band': 0,
                        'original_sentence': [],
                    }
                )

            # Process the transcription using SpaCy
            doc = spacy_service.process_document(transcribe)

            # Define variable to save the cefr classification result
            cefr_classification = []

            # Loop through sentence result from SpaCy
            for sent in doc.sents:
                # Predict the CEFR level
                cefr_band = self._evaluate_cefr_band_classification(sent.text)

                # Predict cefr level each sentence
                cefr_classification.append(cefr_band)

            # Calculate the final band of cefr classification
            lexical_cefr_classification_band = EvRoundedIELTSBand(np.mean(cefr_classification)).rounded_band

            # Tokenize the word using word freq
            words_tokens = wordfreq_tokenize(transcribe, 'en')

            # Get the lexical sophistication information
            lexical_sophistication = self._get_lexical_sophistication(words_tokens)

            # Calculate the words repetition in the words token
            words_repetition = [word for word in words_tokens if words_tokens.count(word) > 1]

            # Calculate the word repetition score
            words_repetition_score = round(len(words_repetition) / len(words_tokens), 3)

            # Get the lexical sophistication band
            lexical_sophistication_ielts_band = self._evaluate_lexical_sophistication(lexical_sophistication, words_repetition_score, len(words_tokens))

            # Rounded to ielts band
            lexical_sophistication_ielts_band = EvRoundedIELTSBand(lexical_sophistication_ielts_band).rounded_band

            # Calculate the lexical diversity
            lexical_diversity_ielts_band = self._evaluate_lexical_diversity(transcribe)

            # Get repetition words in a transcribe
            repetition_words = self._get_repetition_words_without_stop_word(transcribe)

            # Get list of repetition words
            repetition_words_list = list(repetition_words.keys())

            # Evaluate the repetition words
            repetition_words_ielts_band = self._evaluate_repetition_words_without_stop_word(repetition_words)

            # Get the lexical collocation prediction
            lexical_collocation_prediction = self._get_lexical_collocation_prediction(transcribe)

            # Get the lexical collocation score
            lexical_collocation_score = self._get_lexical_collocation_score(lexical_collocation_prediction)

            # Evaluate the lexical collocation score
            lexical_collocation_ielts_band = self._evaluate_lexical_collocation_score(lexical_collocation_score)

            # Define the original sentence
            original_sentence_list = []

            # Loop through the word tokens
            for word in words_tokens:
                # Define flag of the word
                flag = 0

                # If the word is in lexical sophistication advanced
                if word in lexical_sophistication['advanced']:
                    # Set the flag to 0
                    flag = 1

                # If the word is in repetition words
                if word in repetition_words_list:
                    # Set the flag to 0
                    flag = 2

                # Add the word to the original sentence
                original_sentence_list.append((word, flag))

            # Define variable to save the html feedback
            html_original_sentence = ''
            html_correction = ''

            # Loop through the original sentence list
            for word, flag in original_sentence_list:
                # If the flag is 0
                if flag == 0:
                    # Add the word to the html original sentence
                    html_original_sentence += f'{word} '
                # If the flag is 1
                elif flag == 1:
                    # Add the word to the html original sentence
                    html_original_sentence += f"<span style=\"color:green;\">{word}</span> "
                else:
                    # Add the word to the html original sentence
                    html_original_sentence += f"<span style=\"color:red;\">{word}</span> "

            # Strip the html original sentence
            html_original_sentence = html_original_sentence.strip()

            # Check if the lexical sophistication `advanced` is not empty and repetition words list is not empty
            if lexical_sophistication['advanced'] and repetition_words_list:
                # Change the html correction 
                html_correction_lexical_sophistication = ', '.join([
                    f"<span style=\"color:green;\">{word}</span>" for word in lexical_sophistication['advanced']
                ])

                # Add li tag to the html correction
                html_correction = f"<li><p>Advance words: {html_correction_lexical_sophistication}</p></li>"

                # Add the repetition words to the html correction
                html_correction_repetition_words += ', '.join([
                    f"<span style=\"color:red;\">{word}</span>" for word in repetition_words_list
                ])

                # Add li tag to the html correction
                html_correction = f"<li><p>Repetition words: {html_correction_repetition_words}</p></li>"

            # Define variable for final html feedback
            final_html_feedback = f"<p><strong>Original Sentence:</strong></p><p>{html_original_sentence}</p>"

            # Add the correction sentence if it exists
            if html_correction != '':
                final_html_feedback += f"<p><strong>Correction:</strong></p><ul>{html_correction}</ul>"

            # Add div in the feedback
            final_html_feedback = f'<div>{final_html_feedback}</div>'

            # Weighted average
            lexical_score = (
                (lexical_cefr_classification_band * 0.25) +
                (lexical_sophistication_ielts_band * 0.25) +
                (lexical_diversity_ielts_band * 0.2) +
                (repetition_words_ielts_band * 0.2) +
                (lexical_collocation_ielts_band * 0.1)
            )

            # Rounded to ielts band
            final_ielts_band = EvRoundedIELTSBand(lexical_score).rounded_band

            # Return the evaluation model
            return EvEvaluationModel(
                ielts_band = final_ielts_band,
                readable_feedback = final_html_feedback,
                feedback_information = {
                    'cefr_classification': cefr_classification,
                    'lexical_cefr_classification_band': lexical_cefr_classification_band,
                    'lexical_sophistication': lexical_sophistication,
                    'lexical_sophistication_ielts_band': lexical_sophistication_ielts_band,
                    'lexical_diversity_ielts_band': lexical_diversity_ielts_band,
                    'repetition_words': repetition_words,
                    'repetition_words_ielts_band': repetition_words_ielts_band,
                    'lexical_collocation_prediction': lexical_collocation_prediction,
                    'lexical_collocation_score': lexical_collocation_score,
                    'lexical_collocation_ielts_band': lexical_collocation_ielts_band,
                    'original_sentence': original_sentence_list,
                }
            )
        
        except EvException as error:
            # Raise the exception
            raise error
        
        except Exception as error:
            # Define the error message
            message = f'Error evaluating lexical: {str(error)}'

            # Raise an exception with the error message
            raise EvException(
                message = message,
                status_code = 500,
                information = {
                    'message': message,
                }
            )
    
# MARK: LexicalService
# Create the lexical service
lexical_service = LexicalService()