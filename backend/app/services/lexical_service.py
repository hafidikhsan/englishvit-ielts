# Import dependency
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

# Import modules
from config import EvIELTSConfig
from app.utils.exception import EvException
from app.services.spacy_service import spacy_service
from app.utils.rounded_ielts_band import EvRoundedIELTSBand
from app.utils.logger import ev_logger

# MARK: LexicalService
class LexicalService:
    '''
    A class to manage all the lexical IELTS assessment services. This
    class will calculate the lexical score, the IELTS band, feedback.
    '''
    def __init__(self):
        # Class properties
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

            ev_logger.info(f'Successfuly download {self.cefr_classification_model_name} √')

            ev_logger.info(f'Starting download {self.bert_fill_masked_model_name} ...')

            # Get the model
            self.bert_fill_masked_model = pipeline(
                self.bert_fill_masked_model_task,
                self.bert_fill_masked_model_name, 
                token = EvIELTSConfig.hugging_face_api_key,
            )

            ev_logger.info(f'Successfuly download {self.bert_fill_masked_model_name} √')
        except Exception as error:
          ev_logger.info(f'Failed to download models ×')
          ev_logger.info(f'Error: {error}')

    # MARK: CheckModel
    def check_model(self):
        return self.cefr_classification_model is not None and self.cefr_classification_tokenizer is not None and self.bert_fill_masked_model is not None

    # MARK: HealthCheck
    def health_check(self):
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
        # Start download new model
        self._start_download_model()

    # MARK: GetLexicalSophistication
    def _get_lexical_sophistication(self, words: list) -> dict:
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
        # Get the stopword from nltk
        stop_words = set(stopwords.words('english'))

        # Get the word in the transcribe
        words = transcribe.lower().translate(str.maketrans('', '', string.punctuation)).split()

        # Return a list that contain transcribe words without stop words
        return [word for word in words if word not in stop_words]

    # MARK: GetRepetitionWordsWithoutStopword
    def _get_repetition_words_without_stopword(self, transcribe: str) -> dict:
        # Get the content of the words
        words = self._get_content_words(transcribe)

        # Count each word
        word_counts = Counter(words)

        # Return the dict of the repetition words
        return {word: count for word, count in word_counts.items() if count > 1}
    
    # MARK: GetLexicalCollocationPrediction
    def _get_lexical_collocation_prediction(self, transcribe: str) -> list:
        # Get the stopword from nltk
        stop_words = set(stopwords.words('english'))

        # Tokenize the transcribe
        sentences = sent_tokenize(transcribe)

        # Define variable to store the lexial collocation prediction
        lexical_collocation_prediction = []

        # Loop through the sentences
        for sentence in sentences:
            # Word tokenize the sentence
            word_tokenize_sentence = word_tokenize(sentence)

            # Tagging the sentence
            word_pos_tags = pos_tag(word_tokenize_sentence)

            # Define variable to save the the potential masked and masked predict result
            potential_masked = []
            masked_predict = []

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

                    # Add the predict in the lexical collcoation predict
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
        # If the prediction is empty return 0
        if not lexical_collocation_prediction:
            return 0

        return round((sum([1 for pred in lexical_collocation_prediction if pred[0]]) / len(lexical_collocation_prediction)) * 100, 3)

    # MARK: EvaluateLexicalSophistication
    def _evaluate_lexical_sophistication(self, distribution: dict, repetition_score: float, total_words: float) -> float:
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
    def _evaluate_cefr_band_classification(self, transcribe: str) -> tuple[float, str]:
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
        return (EvRoundedIELTSBand(cefr_to_ielts[label]).rounded_band, label)

    # MARK: EvaluateLexicalDiversity
    def _evaluate_lexical_diversity(self, transcribe: str) -> float:
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

    # MARK: EvaluateRepetitionWordsWithoutStopword
    def _evaluate_repetition_words_without_stopword(self, repetition_words: dict) -> float:
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

    # MARK: Score
    def score(self, transcribe: str) -> tuple[float, str]:
        # If the transcribe is empty or words is empty
        if transcribe == '' or not transcribe: 
            return (0, 'Not detect a speech.')

        # Define a text to save the information evaluation of the dictionary
        feedback = ''

        # Process the transcription using SpaCy
        doc = spacy_service.process_document(transcribe)

        # Define variable to save the cefr classification result
        cefr_classification = []

        # Add the total words to the feedback
        feedback += f'Candidate have speech transcribe, '

        # Define variable to save the feebcak cefr classification
        feedback_cefr_classification = []

        # Loop through sentence result from SpaCy
        for index, sent in enumerate(doc.sents):
            # Predict the CEFR level
            cefr_band, cefr_level = self._evaluate_cefr_band_classification(sent.text)

            # Predict cefr level each sentence
            cefr_classification.append(cefr_band)

            # Add to the feedback
            feedback_cefr_classification.append(f'sentence [{sent.text}] with mapping ti CEFR level is {cefr_level}')

        # Add cefr classification feedback to the feedback
        feedback += ', '.join(feedback_cefr_classification) + '. '

        # Calculate the final band of cefr classification
        lexical_cefr_classification_band = EvRoundedIELTSBand(np.mean(cefr_classification)).rounded_band

        # Add the final band of cefr classification to the feedback
        feedback += f'Get final IELTS band based of our system and cefr classification is {lexical_cefr_classification_band}. '

        # Tokenize the word using word freq
        words_tokens = wordfreq_tokenize(transcribe, 'en')

        # Get the lexical sophistication information
        lexical_sophistication = self._get_lexical_sophistication(words_tokens)

        # Add the lexical sophistication information to the feedback
        feedback += f'Get lexical sophistication information is, '

        # Loop through the lexical sophistication information
        for key, value in lexical_sophistication.items():
            # Check if have value
            if value:
                # Get the string of the words in value
                words_value = ', '.join(set(value))

                # Add the lexical sophistication information to the feedback
                feedback += f'{key}: {words_value}, '
            else:
                # Add the lexical sophistication information to the feedback
                feedback += f'{key}: None, '

        # Calculate the words repetition in the words token
        words_repetition = [word for word in words_tokens if words_tokens.count(word) > 1]

        # Calculate the word repetition score
        words_repetition_score = round(len(words_repetition) / len(words_tokens), 3)

        # Get the lexical sophistication band
        lexical_sophistication_ielts_band = self._evaluate_lexical_sophistication(lexical_sophistication, words_repetition_score, len(words_tokens))

        # Rounded to ielts band
        lexical_sophistication_ielts_band = EvRoundedIELTSBand(lexical_sophistication_ielts_band).rounded_band

        # Add the lexical sophistication band
        feedback += f'Get final IELTS band based of our system and lexical sophistication is {lexical_sophistication_ielts_band}. '

        # Calculate the lexical diversity
        lexical_diversity_ielts_band = self._evaluate_lexical_diversity(transcribe)

        # Add the lexical diversity to the feedback
        feedback += f'Get final IELTS band based of our system and lexical diversity is {lexical_diversity_ielts_band}. '

        # Get repetition words in a transcribe
        repetition_words = self._get_repetition_words_without_stopword(transcribe)

        # Evaluate the repetition words
        repetition_words_ielts_band = self._evaluate_repetition_words_without_stopword(repetition_words)

        # Get the word and counter of the word repetition
        repetition_words_counter = ', '.join([f'{word}: {count}' for word, count in repetition_words.items()])

        # Add repetition words in a transcribe to the feedback
        feedback += f'Fined repetition words in a transcribe is {repetition_words_counter}. '

        # Add the repetition words ielts band to the feedback
        feedback += f'Get final IELTS band based of our system and repetition words is {repetition_words_ielts_band}. '

        # Get the lexical collocation prediction
        lexical_collocation_prediction = self._get_lexical_collocation_prediction(transcribe)

        # Get the lexical collocation score
        lexical_collocation_score = self._get_lexical_collocation_score(lexical_collocation_prediction)

        # Ecaluate the lexical collocation score
        lexical_collocation_ielts_band = self._evaluate_lexical_collocation_score(lexical_collocation_score)

        # Define variable to check the collocation
        feedback_lexical_collocation = []

        # Loop through the prediction
        for result in lexical_collocation_prediction:
            # Decode the result
            is_correct, _, _, sentence = result

            # Check if not correct
            if not is_correct:
                # Add the sentence to the feedback
                feedback_lexical_collocation.append(f'[{sentence}]')

        # Check if get feedback
        if feedback_lexical_collocation:
            # Add the lexical collocation prediction to the feedback
            feedback += f'Get some missing collocation in '
            feedback += ', '.join(set(feedback_lexical_collocation))
            feedback += '. '

        # Add the lexical collocation ielts band in the feedback
        feedback += f'Get final IELTS band based of our system and lexical collocation is {lexical_collocation_ielts_band}. '

        # Weighted average
        lexical_score = (
            (lexical_cefr_classification_band * 0.25) +
            (lexical_sophistication_ielts_band * 0.25) +
            (lexical_diversity_ielts_band * 0.2) +
            (repetition_words_ielts_band * 0.2) +
            (lexical_collocation_ielts_band * 0.1)
        )

        # Rounde to ielts band
        lexical_score = EvRoundedIELTSBand(lexical_score).rounded_band

        # Add the lexical score to the feedback
        feedback += f'Get final IELTS band based of our system and lexical score is {lexical_score}.'

        # Return the feedback
        return (lexical_score, feedback)
    
# MARK: LexicalService
# Create the lexical service
lexical_service = LexicalService()