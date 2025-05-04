# Import dependency
import datetime
import statistics
from difflib import SequenceMatcher
from transformers import (
    pipeline,
    AutoTokenizer,
    T5ForConditionalGeneration,
)
from happytransformer import (
    HappyTextToText,
    TTSettings,
)

# Import modules
from config import EvIELTSConfig
from app.utils.exception import EvException
from app.services.spacy_service import spacy_service
from app.utils.rounded_ielts_band import EvRoundedIELTSBand
from app.utils.logger import ev_logger

# MARK: GrammarService
class GrammarService:
    '''
    A class to manage all the grammar IELTS assessment services. This
    class will calculate the grammar score, the IELTS band, feedback.
    '''
    def __init__(self):
        # Class properties
        self.grammarly_model_name = EvIELTSConfig.grammar_grammarly_gec_model_name
        self.grammarly_model = None
        self.grammarly_tokenizer = None
        self.happy_base_model_name = EvIELTSConfig.grammar_happy_gec_base_model_name
        self.happy_model_name = EvIELTSConfig.grammar_happy_gec_model_name
        self.happy_model = None
        self.open_source_model_name = EvIELTSConfig.grammar_open_source_gec_model_name
        self.open_source_model_task = EvIELTSConfig.grammar_open_source_gec_model_task
        self.open_source_pipeline = None
        self.tokenizer_max_length = EvIELTSConfig.tokenizer_max_length

        # Start download the model
        self._start_download_model()

    # MARK: StartDownloadModel
    def _start_download_model(self):
        try:
            ev_logger.info(f'Starting download {self.grammarly_model_name} ...')

            # Get the tokenizer
            self.grammarly_tokenizer = AutoTokenizer.from_pretrained(
                self.grammarly_model_name, 
                token = EvIELTSConfig.hugging_face_api_key
            )

            # Get the model
            self.grammarly_model = T5ForConditionalGeneration.from_pretrained(
                self.grammarly_model_name, 
                token = EvIELTSConfig.hugging_face_api_key
            )

            ev_logger.info(f'Successfuly download {self.grammarly_model_name} √')

            ev_logger.info(f'Starting download {self.happy_model_name} ...')

            # Get the model
            self.happy_model = HappyTextToText(
                self.happy_base_model_name, 
                self.happy_model_name
            )

            ev_logger.info(f'Successfuly download {self.grammarly_model_name} √')

            ev_logger.info(f'Starting download {self.open_source_model_name} ...')

            # Get the model
            self.open_source_pipeline = pipeline(
                self.open_source_model_task,
                self.open_source_model_name, 
                token = EvIELTSConfig.hugging_face_api_key
            )

            ev_logger.info(f'Successfuly download {self.open_source_model_name} √')
        except Exception as error:
          ev_logger.info(f'Failed to download models ×')
          ev_logger.info(f'Error: {error}')

    # MARK: CheckModel
    def check_model(self):
        return self.grammarly_tokenizer is not None and self.grammarly_model is not None and self.happy_model is not None and self.open_source_pipeline is not None

    # MARK: HealthCheck
    def health_check(self):
        return {
            'grammarly_model_ready': self.grammarly_model is not None and self.grammarly_tokenizer is not None,
            'grammarly_model_name': self.grammarly_model_name,
            'grammarly_base_model': 'T5',
            'grammarly_model_type': 'T5ForConditionalGeneration',
            'grammarly_tokenizer_type': 'AutoTokenizer',
            'grammarly_model_description': 'Perform GEC using open source grammarly',
            'happy_model_ready': self.happy_model is not None,
            'happy_model_name': self.happy_model_name,
            'happy_base_model': 'T5',
            'happy_model_type': 'HappyTextToText',
            'happy_model_description': 'Perform GEC using open source Happy T5',
            'open_source_model_ready': self.open_source_pipeline is not None,
            'open_source_model_name': self.open_source_model_name,
            'open_source_base_model': 'T5',
            'open_source_model_description': 'Perform GEC using open source',
            'time_stamp': datetime.datetime.now()
        }
        
    # MARK: UpdateModel
    def update_model(self):
        # Start download new model
        self._start_download_model()

    # MARK: GetGrammarCorrection
    def _get_grammar_correction(self, transcribe_text: str, model_type: str = 'base') -> str:
        # If the model use happy transformer
        if model_type == 'happy':
            # Define arguments for the Happy transformer model
            args = TTSettings(
                num_beams = 5,
                min_length = 1
            )

            # Inference the text and add the prefix "grammar: " before each input
            result = self.happy_model.generate_text(
                'grammar: ' + transcribe_text,
                args = args
            )

            # Return the GEC
            return result.text

        # If the model use grammarly
        elif model_type == 'grammarly':
            # Tokenize the input
            grammar_correction_input_ids = self.grammarly_tokenizer(
                'Fix the grammar: ' + transcribe_text,
                return_tensors = 'pt'
            ).input_ids

            # Inference the GEC model
            outputs = self.grammarly_model.generate(
                grammar_correction_input_ids,
                max_length = self.tokenizer_max_length,
            )

            # Get the grammar correction
            grammar_currector_output = self.grammarly_tokenizer.decode(
                outputs[0],
                skip_special_tokens = True
            )

            # Return the GEC
            return grammar_currector_output

        # Else using open source GEC model
        else:
            # Inference the model
            result_gec = self.open_source_pipeline(
                transcribe_text,
                max_length = self.tokenizer_max_length,
                num_beams = 5,
                no_repeat_ngram_size = 2
            )

            # Return the GEC
            return ' '.join(result['generated_text'] for result in result_gec)

    # MARK: GetGrammarErrorInformation
    def _get_grammar_error_information(self, transcribe_list: list, correction_list: list) -> list:
        # Define variable to get the error and list of feedback
        feedbacks = []

        # Find differences using SequenceMatcher
        matcher = SequenceMatcher(None, transcribe_list, correction_list)

        # Loop through the matcher result
        for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
            if opcode in ['replace', 'delete', 'insert']:
                # Generate feedback for each error
                if opcode == 'replace':
                    feedbacks.append({
                        'error_type': opcode,
                        'original_phrase': ' '.join(transcribe_list[i1:i2]),
                        'corrected_phrase': ' '.join(correction_list[j1:j2]),
                        'message': 'Replace the word [' + ' '.join(transcribe_list[i1:i2]) + '] with [' + ' '.join(correction_list[j1:j2]) + ']',
                    })
                elif opcode == 'delete':
                    feedbacks.append({
                        'error_type': opcode,
                        'original_phrase': ' '.join(transcribe_list[i1:i2]),
                        'corrected_phrase': '',
                        'message': 'Delete the word [' + ' '.join(transcribe_list[i1:i2]) + ']',
                    })
                elif opcode == 'insert':
                    feedbacks.append({
                        'error_type': opcode,
                        'original_phrase': '',
                        'corrected_phrase': ' '.join(correction_list[j1:j2]),
                        'message': 'Insert the word [' + ' '.join(correction_list[j1:j2]) + ']',
                    })

        # Return the feedback
        return feedbacks

    # MARK: GetGrammarErrorRate
    def _get_grammar_error_rate(self, feedbacks: list, transcribe_length: int) -> float:
        # If the feedback is empty
        if len(feedbacks) == 0:
            # Give 0 error rate bacause none text difference
            return 0

        # Define list to store the error rates (int)
        insertions = []
        deletions = []
        replaces = []

        # Get the error rate based on the error type
        for feedback in feedbacks:
            # Get the error type
            error_type = feedback['error_type']

            # If the error type is insertion
            if error_type == 'insert':
                # Get the insertion words lenght
                added_word = len(feedback['corrected_phrase'])

                # Calculate the error rate
                insertions.append(added_word / (transcribe_length + added_word))

            # If the error type is deletion
            elif error_type == 'delete':
                # Get the deletion words lenght
                deleted_word = len(feedback['original_phrase'])

                # Calculate the error rate
                deletions.append(deleted_word / transcribe_length)

            # If the error type is substitution
            elif error_type == 'replace':
                # Get the replace words lenght
                original_word = len(feedback['original_phrase'])
                corrected_word = len(feedback['corrected_phrase'])

                # Calculate the error rate
                replaces.append(abs(original_word - corrected_word) / transcribe_length)

        # Define mean of each error type
        insertions_mean = statistics.mean(insertions) if len(insertions) > 0 else 0
        deletions_mean = statistics.mean(deletions) if len(deletions) > 0 else 0
        replaces_mean = statistics.mean(replaces) if len(replaces) > 0 else 0

        # Return the grammar error rate
        return statistics.mean([insertions_mean, deletions_mean, replaces_mean])

    # MARK: GetSentenceStructure
    def _get_sentence_structure(self, sentence: list) -> str:
        # Count subordinate clause markers
        num_dependent = sum(1 for token in sentence if token.dep_ in ['advcl', 'relcl', 'ccomp', 'xcomp', 'acl'])

        # Count coordinating conjunctions
        num_coordinators = sum(1 for token in sentence if token.dep_ == 'cc')

        # Score the sentence sentence based on subordinate clause markers and coordinating conjunctions
        if num_dependent > 0 and num_coordinators > 0:
            return 'Compound-Complex'
        elif num_dependent > 0:
            return 'Complex'
        elif num_coordinators > 0:
            return 'Compound'
        else:
            return 'Simple'

    # MARK: GetGrammarFeature
    def _get_grammar_feature(self, sentence: list) -> dict:
        # Define the list of the grammar feature
        grammar_feature_modal = []
        grammar_feature_passive = []
        grammar_feature_conditional = []
        grammar_feature_relative = []

        # Define some conditional text
        conditional_triggers = [
            'if', 'unless', 'provided', 'providing', 'assuming', 'as long as', 'even if', 'in case', 'on condition that', 'supposing', 'suppose', 'whether or not', 'only if',
        ]

        # Loop through the sentence
        for token in sentence:
            # If tag is a modal
            if token.tag_ == 'MD':
                # Add the text to grammar feature modal list
                grammar_feature_modal.append(token.text)

            # If tag is a passive
            if token.dep_ == 'auxpass':
                # Add the text to grammar feature passive list
                grammar_feature_passive.append(token.text)

            # If tag is a conditional
            if token.text.lower() in conditional_triggers:
                # Add the text to grammar feature conditional list
                grammar_feature_conditional.append(token.text)

            # If tag is a relative
            if token.dep_ == 'relcl':
                # Add the text to grammar feature relative list
                grammar_feature_relative.append(token.text)

        return {
            'modal': grammar_feature_modal,
            'passive': grammar_feature_passive,
            'conditional': grammar_feature_conditional,
            'relative': grammar_feature_relative,
        }

    # MARK: GetGrammarSentenceTense
    def _get_grammar_sentence_tense(self, sentence: list) -> dict:
        # Define the list of the grammar sentence tense
        grammar_tense_present_simple = []
        grammar_tense_present_continuous = []
        grammar_tense_present_perfect = []
        grammar_tense_present_perfect_continuous = []
        grammar_tense_past_simple = []
        grammar_tense_past_continuous = []
        grammar_tense_past_perfect = []
        grammar_tense_past_perfect_continuous = []
        grammar_tense_future_simple = []
        grammar_tense_future_continuous = []
        grammar_tense_future_perfect = []
        grammar_tense_future_perfect_continuous = []

        # Loop through the sentence
        for token in sentence:
            # If tag is a verb
            if token.tag_ in ['VBD', 'VBN', 'VBZ', 'VBP', 'VB', 'VBG']:
                # Get the auxilary
                aux = [child for child in token.children if child.dep_ in ('aux', 'auxpass')]
                aux_text = ' '.join([a.text.lower() for a in aux])

                # Define the verb tag
                verb_tag = token.tag_

                # Present Simple
                if verb_tag in ['VBZ', 'VBP']:
                    if 'have been' in aux_text:
                        grammar_tense_present_perfect_continuous.append(token.text)
                    elif 'have' in aux_text or 'has' in aux_text:
                        grammar_tense_present_perfect.append(token.text)
                    elif 'am' in aux_text or 'is' in aux_text or 'are' in aux_text:
                        grammar_tense_present_continuous.append(token.text)
                    else:
                        grammar_tense_present_simple.append(token.text)

                # Past Tenses
                elif verb_tag == 'VBD':
                    if 'was' in aux_text or 'were' in aux_text:
                        grammar_tense_past_continuous.append(token.text)
                    elif 'had been' in aux_text:
                        grammar_tense_past_perfect_continuous.append(token.text)
                    elif 'had' in aux_text:
                        grammar_tense_past_perfect.append(token.text)
                    else:
                        grammar_tense_past_simple.append(token.text)

                # Future Tenses
                elif 'will have been' in aux_text:
                    grammar_tense_future_perfect_continuous.append(token.text)
                elif 'will have' in aux_text:
                    grammar_tense_future_perfect.append(token.text)
                elif 'will be' in aux_text:
                    grammar_tense_future_continuous.append(token.text)
                elif 'will' in aux_text:
                    grammar_tense_future_simple.append(token.text)

        return {
            'present_simple': grammar_tense_present_simple,
            'present_continuous': grammar_tense_present_continuous,
            'present_perfect': grammar_tense_present_perfect,
            'present_perfect_continuous': grammar_tense_present_perfect_continuous,
            'past_simple': grammar_tense_past_simple,
            'past_continuous': grammar_tense_past_continuous,
            'past_perfect': grammar_tense_past_perfect,
            'past_perfect_continuous': grammar_tense_past_perfect_continuous,
            'future_simple': grammar_tense_future_simple,
            'future_continuous': grammar_tense_future_continuous,
            'future_perfect': grammar_tense_future_perfect,
            'future_perfect_continuous': grammar_tense_future_perfect_continuous,
        }

    # MARK: GetSentenceFunction
    def _get_sentence_function(self, sentence: list) -> str:
        # Cleaning the text
        text = sentence.text.strip()

        # Define the senten function based on the text information
        if text.endswith('?'):
            return 'Interrogative'
        elif text.endswith('!') or any(word.lower() in text.lower() for word in ['what', 'how']):
            return 'Exclamatory'
        elif text.split()[0].lower() in ['please', 'do', 'stop', 'go', 'turn', 'be', 'make'] or sentence[0].lemma_ in ['please', 'do', 'let', 'be'] or sentence[0].tag_ == 'VB':
            return 'Imperative'
        else:
            return 'Declarative'
    
    # MARK: EvaluateGrammarErrorRate
    def _evaluate_grammar_error_rate(self, error_rate: int) -> float:
        # Mapping the error rate to get ielts Band
        if error_rate < .02: return 9
        elif error_rate < .05: return 8
        elif error_rate < .1: return 7
        elif error_rate < .2: return 6
        elif error_rate < .3: return 5
        elif error_rate < .4: return 4
        elif error_rate < .5: return 3
        elif error_rate < .6: return 2
        else: return 1

    # MARK: EvaluateGrammarSentenceStructure
    def _evaluate_grammar_sentence_structure(self, grammar_sentence_structures: list) -> float:
        # Define variable to save the IELTS band
        ielts_band = 0

        # If the list ie empty, give IELTS band to 0
        if len(grammar_sentence_structures) == 0:
            return ielts_band

        # Count total of the sentence
        total = len(grammar_sentence_structures)

        # Calculate the ratio of complex and coumpoune complex
        ratio_complex = (grammar_sentence_structures.count('Complex') + grammar_sentence_structures.count('Compound-Complex')) / total
        ratio_simple = grammar_sentence_structures.count('Simple') / total

        # Mapping the IELTS band based on the grammar sentence structure
        if ratio_complex == 0:
            if ratio_simple <= .5:
                ielts_band = 1
            elif ratio_simple <= .75:
                ielts_band = 2
            else:
                ielts_band = 3
        elif ratio_complex <= .25:
            ielts_band = 4
        elif ratio_complex <= .5:
            ielts_band = 5
        elif ratio_complex <= .75:
            ielts_band = 6
        else:
            if grammar_sentence_structures.count('Compound-Complex') >= 3:
                ielts_band = 9
            elif grammar_sentence_structures.count('Compound-Complex') >= 1:
                ielts_band = 8
            else:
                ielts_band = 7

        return ielts_band
    
    # MARK: EvaluateGrammarFeature
    def _evaluate_grammar_feature(self, grammar_features: set) -> float:
        # Assign weights based on complexity
        weights = {
            'modal': 1.0,
            'passive': 1.5,
            'conditional': 2.0,
            'relative': 2.0,
        }

        # Define the max weight
        max_weighted_score = sum(weights.values())

        # Define value to save the actual score
        actual_score = 0.0

        # Loop through the grammar features
        for feat in grammar_features:
            # If the feature is included in the sentence
            if feat in weights:
                # Add the feature weight in the actual score
                actual_score += weights[feat]

        # Calculate the ratio
        ratio = actual_score / max_weighted_score

        # Map ratio to band
        if ratio == 0:
            return 3
        elif ratio < 0.3:
            return 4
        elif ratio < 0.5:
            return 5
        elif ratio < 0.7:
            return 6
        elif ratio < 0.85:
            return 7
        elif ratio < 1.0:
            return 8
        else:
            return 9
    
    # MARK: EvaluateGrammarTense
    def _evaluate_grammar_tenses(self, grammar_tenses: set) -> float:
        # Define the length of the tenses
        tenses_length = len(grammar_tenses)

        # Mapping the tenses to IELTS band
        if tenses_length <= 1:
            return 3
        elif tenses_length <= 2:
            return 4
        elif tenses_length <= 3:
            return 5
        elif tenses_length <= 4:
            return 6
        elif tenses_length <= 5:
            return 7
        elif tenses_length <= 6:
            return 8
        else:
            return 9
    
    # MARK: EvaluateGrammarFunction
    def _evaluate_grammar_function(self, grammar_functions: dict) -> float:
        # Count the variety
        count_variety = sum(1 for count in grammar_functions.values() if count > 0)

        # Adjust the range as per the variety of functions
        if count_variety == 4:
            return 9
        elif count_variety == 3:
            return 8
        elif count_variety == 2:
            return 7
        elif count_variety == 1:
            return 6
        else:
            return 5

    # Score
    def score(self, transcribe: str) -> tuple[float, str]:
        # If the transcribe is empty or words is empty
        if transcribe == '' or not transcribe: 
            return (0, 'Not detect a speech.')

        # Process the transcription using SpaCy
        sentences = spacy_service.process_document(transcribe)

        # Define variable to save the feedback
        feedbacks = []

        # Loop through sentence result from SpaCy
        for sentence in sentences.sents:
            # Define a text to save the information evaluation
            feedback = f'In sentence [{sentence.text}], '

            # Get the GEC result
            correction_text = self._get_grammar_correction(sentence.text)

            # Add the correction to the feedback
            feedback += f'get correction [{correction_text}]. '

            # Split the transcribe and correction text
            transcribe_tokens = sentence.text.split()
            correction_tokens = correction_text.split()

            # Define grammar accuracy ielts band and feedback
            grammar_accuracy_band = 0
            grammar_accuracy_feedbacks = []

            # Check if the transcribe is empty
            if len(transcribe_tokens) <= 0:
                # Add the feedback
                feedback += 'Transcribe is empty and get final IELTS band based of our system and grammar accuracy is 0. '

            else:
                # Identify the grammar error feedback list
                grammar_accuracy_feedbacks_original = self._get_grammar_error_information(transcribe_tokens, correction_tokens)

                # Get the error rate
                error_rate = self._get_grammar_error_rate(grammar_accuracy_feedbacks_original, len(transcribe_tokens))

                # Convert the error rate to IELTS Band
                grammar_accuracy_band = self._evaluate_grammar_error_rate(error_rate)

                # Add the feedback of the grammar accuracy
                grammar_accuracy_feedbacks.extend([feedback['message'] for feedback in grammar_accuracy_feedbacks_original])

                # Check if empty accuracy feedback
                if len(grammar_accuracy_feedbacks) == 0:
                    # Add the feedback
                    feedback += f'There is no feedback and get the grammar accuracy band is {grammar_accuracy_band}. '

                else:
                    # Add the the feedback
                    feedback += 'Get some grammar error: ' + ', '.join(grammar_accuracy_feedbacks) + '. '
                    feedback += f'Get the grammar accuracy band is {grammar_accuracy_band}. '

            # Get the grammar range structure
            grammar_range_structure = self._get_sentence_structure(sentence)

            # Add to the feedback
            feedback += f'This sentence is {grammar_range_structure} sentence, '

            # Get the grammar range feature
            grammar_range_feature = self._get_grammar_feature(sentence)

            # Define grammar range feature feedback
            grammar_range_feature_feedback = []

            # Loop through the feature
            for key in grammar_range_feature.keys():
                # Check if the feature count more than 1
                if len(grammar_range_feature[key]) > 0:
                    # Add to the grammar range feature feedback
                    grammar_range_feature_feedback.append(key)

            # Check if empty grammar range feature feedback
            if len(grammar_range_feature_feedback) > 0:
                # Add to the feedback
                feedback += f'have ' +  ', '.join(grammar_range_feature_feedback) + f' sentence, '

            # Get the grammar range tenses
            grammar_range_tenses = self._get_grammar_sentence_tense(sentence)

            # Define grammar range tenses feedback
            grammar_range_tenses_feedback = []

            # Loop through the tenses
            for key in grammar_range_tenses.keys():
                # Check if the tenses count more than 1
                if len(grammar_range_tenses[key]) > 0:
                    # Add to the grammar range tenses feedback
                    grammar_range_tenses_feedback.append(key)

            # Check if empty grammar range tenses feedback
            if len(grammar_range_tenses_feedback) > 0:
                # Add to the feedback
                feedback += f'have ' +  ', '.join(grammar_range_tenses_feedback) + f' sentence, '

            # Get the grammar range functions
            grammar_range_function = self._get_sentence_function(sentence)

            # Add to the feedback
            feedback += f'and {grammar_range_function} sentence. '

            # Add to feedback data
            feedbacks.append({
                'sentence': sentence.text,
                'correction': correction_text,
                'grammar_accuracy_band': grammar_accuracy_band,
                'grammar_accuracy_feedbacks': grammar_accuracy_feedbacks,
                'grammar_range_structure': grammar_range_structure,
                'grammar_range_feature': grammar_range_feature,
                'grammar_range_tenses': grammar_range_tenses,
                'grammar_range_function': grammar_range_function,
                'feedback': feedback,
            })

        # If the length of the feedback is 0
        if len(feedbacks) == 0:
            # Return ielts band 0
            return (0, 'No feedback')

        else:
            # Define a text to save the information evaluation
            feedback = ''.join([feedback['feedback'] for feedback in feedbacks])

            # Get the grammar accuracy IELTS band
            final_grammar_accuracy_band = EvRoundedIELTSBand(statistics.mean([feedback['grammar_accuracy_band'] for feedback in feedbacks]) if len(feedbacks) > 0 else 0).rounded_band

            # Add to the feedback
            feedback += f'Get final IELTS band based of our system and grammar accuracy is {final_grammar_accuracy_band}. '

            # Get the grammar range structures IELTS band
            final_grammar_range_structure_band = self._evaluate_grammar_sentence_structure([feedback['grammar_range_structure'] for feedback in feedbacks])

            # Add to the feedback
            feedback += f'Get final IELTS band based of our system and grammar structure range is {final_grammar_range_structure_band}. '

            # Define set to score the grammar feature and tenses
            final_grammar_feature_band_data = set()
            final_grammar_tenses_band_data = set()

            # Define dictionary to score the grammar functions
            final_grammar_functions_data = {
                'Interrogative': 0,
                'Exclamatory': 0,
                'Imperative': 0,
                'Declarative': 0,
            }

            # Loop through the feedback list
            for feedback_data in feedbacks:
                # Get the features and tenses feedback
                features = feedback_data['grammar_range_feature']
                tenses = feedback_data['grammar_range_tenses']

                # Loop through the grammar feature feedback
                for key in features.keys():
                    # Check if the feedback feature count more than 1
                    if len(features[key]) > 0:
                        # Add key to the grammar feature band
                        final_grammar_feature_band_data.add(key)

                # Loop through the grammar tenses feedback
                for key in tenses.keys():
                    # Check if the feedback tenses count more than 1
                    if len(tenses[key]) > 0:
                        # Add key to the grammar tenses band
                        final_grammar_tenses_band_data.add(key)

                # Get the sentence function feedback
                final_grammar_functions_data[feedback_data['grammar_range_function']] += 1


            # Get the grammar feature IELTS band
            final_grammar_feature_band = self._evaluate_grammar_feature(final_grammar_feature_band_data)

            # Add to the feedback
            feedback += f'Get final IELTS band based of our system and grammar feature range is {final_grammar_feature_band}. '

            # Get the grammar tenses IELTS band
            final_grammar_tenses_band = self._evaluate_grammar_tenses(final_grammar_tenses_band_data)

            # Add to the feedback
            feedback += f'Get final IELTS band based of our system and grammar tenses range is {final_grammar_tenses_band}. '

            # Get the grammar functions IELTS band
            final_grammar_functions_band = self._evaluate_grammar_function(final_grammar_functions_data)

            # Add to the feedback
            feedback += f'Get final IELTS band based of our system and grammar functions range is {final_grammar_functions_band}. '

            # Get final grammar band
            final_grammar_range_band = EvRoundedIELTSBand(
                (final_grammar_range_structure_band * 0.5) +
                (final_grammar_feature_band * 0.3) +
                (final_grammar_tenses_band * 0.1) +
                (final_grammar_functions_band * 0.1)
            ).rounded_band

            # Get the final IELTS Band
            grammar_score = EvRoundedIELTSBand(
                (final_grammar_accuracy_band * 0.5) +
                (final_grammar_range_band * 0.5)
            ).rounded_band

            # Add to the feedback
            feedback += f'Get final IELTS band based of our system and grammar score is {grammar_score}. '

            # Return the feedback
            return (grammar_score, feedback)
        
# MARK: GrammarService
# Create a grammar service instance
grammar_service = GrammarService()