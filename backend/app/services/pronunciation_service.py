# MARK: Imports
# Dependencies
import os
import subprocess
import numpy as np
from textgrid import TextGrid

# Modules
from app.models.evaluation_model import EvEvaluationModel
from app.utils.exception import EvServerException
from app.utils.rounded_ielts_band import EvRoundedIELTSBand

# MARK: PronunciationService
class PronunciationService:
    '''
    PronunciationService is a class that provides methods for evaluating pronunciation of an
    IELTS speaking simulation. It uses the EvEvaluationModel to structure the evaluation results. 
    The class includes properties for the evaluation model, as well as methods for evaluating 
    pronunciation.
    '''
    # MARK: Properties
    def __init__(self):
        '''
        Initializes the PronunciationService with an EvEvaluationModel instance.
        '''
        self.tool = 'mfa'
        self.task = 'align'
        self.acoustic_model = self.dictionary = 'english_us_arpa'
        self.tags = '--clean --single_speaker --workers 2'
        self.results_file_extension = 'TextGrid'
        self.phoneme_threshold = 0.06
        self.arpabert_to_ipa = {
            'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ',
            'AW': 'aʊ', 'AY': 'aɪ', 'B': 'b', 'CH': 'tʃ',
            'D': 'd', 'DH': 'ð', 'EH': 'ɛ', 'ER': 'ɝ',
            'EY': 'eɪ', 'F': 'f', 'G': 'ɡ', 'HH': 'h',
            'IH': 'ɪ', 'IY': 'i', 'JH': 'dʒ', 'K': 'k',
            'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ŋ',
            'OW': 'oʊ', 'OY': 'ɔɪ', 'P': 'p', 'R': 'ɹ',
            'S': 's', 'SH': 'ʃ', 'T': 't', 'TH': 'θ',
            'UH': 'ʊ', 'UW': 'u', 'V': 'v', 'W': 'w',
            'Y': 'j', 'Z': 'z', 'ZH': 'ʒ'
        }

    # MARK: MapPronounceToIELTSBand
    def _map_pronounce_to_ielts_band(
            self, 
            phoneme_count: int, 
            phoneme_error_count: int, 
            missing_phoneme_count: int,
        ) -> int:
        '''
        Maps pronounce evaluation metrics to an IELTS band.
        '''
        # Adjust phoneme and word counts to include missing ones
        total_phoneme_count = phoneme_count + missing_phoneme_count

        # Calculate error rates
        phoneme_error_rate = (phoneme_error_count + missing_phoneme_count) / total_phoneme_count if total_phoneme_count > 0 else 1

        # Define thresholds for IELTS bands based on phoneme error rate
        if phoneme_error_rate < 0.05:
            return 9
        elif phoneme_error_rate < 0.1:
            return 8
        elif phoneme_error_rate < 0.15:
            return 7
        elif phoneme_error_rate < 0.2:
            return 6
        elif phoneme_error_rate < 0.3:
            return 5
        elif phoneme_error_rate < 0.4:
            return 4
        elif phoneme_error_rate < 0.5:
            return 3
        elif phoneme_error_rate < 0.7:
            return 2
        else:
            return 1
        
    # MARK: MapConfidenceToIELTSBand
    def _map_confidence_to_ielts_band(self, avg_confidence: float) -> int:
        '''
        Maps the average word confidence to an IELTS band.
        '''
        # Define thresholds for IELTS bands based on average confidence score
        if avg_confidence > 0.9:
            return 9
        elif avg_confidence > 0.8:
            return 8
        elif avg_confidence > 0.7:
            return 7
        elif avg_confidence > 0.6:
            return 6
        elif avg_confidence > 0.5:
            return 5
        elif avg_confidence > 0.4:
            return 4
        elif avg_confidence > 0.3:
            return 3
        elif avg_confidence > 0.2:
            return 2
        else:
            return 1
        
    # MARK: GenerateHTMLFeedback
    def _generate_html_feedback(
            self, 
            word_level_feedback: list,
            final_ielts_band: float,
        ) -> str:
        '''
        Generates an HTML feedback report based on the evaluation results.
        '''
        # Define the original sentence
        original_sentence = ''

        # Define the phoneme error data
        phoneme_error = []

        # Loop through the word level feedback
        for word_data in word_level_feedback:
            # Define a flag to know if the word have missing phonemes
            is_true = True

            # Define the word
            word = word_data['word']

            # Define phonemes of the word
            phonemes = ''

            # Loop through the phonemes
            for ph in word_data['phonemes']:
                # Get the phoneme
                ph_ipa = ph['ipa']

                # Check if the phoneme is not pronounced
                if ph['status'] == 0:
                    # Set the flag to False
                    is_true = False
                    
                    # Add the phoneme to the phonemes string with red color
                    phonemes += f"<span style=\"color:red;\">{ph_ipa}</span>"
                else:
                    # Add the phoneme to the phonemes string
                    phonemes += f"{ph_ipa}"
            
            # Check if the word does not have missing phonemes
            if is_true:
                # Add the original sentence with the word
                original_sentence += f"{word} "
            else:
                # Add the original sentence with the word but using red color
                original_sentence += f"<span style=\"color:red;\">{word}</span> "

                # Add the phoneme error data
                phoneme_error.append((
                    word, 
                    f"/{phonemes}/",
                ))
        
        # Strip the original sentence and add HTML tags
        original_sentence = original_sentence.strip()

        # Add tags to the original sentence
        original_sentence = '<p>' + original_sentence + '</p>'

        # Define the HTML of the correction
        correction_sentence = ''

        # Check if the phoneme error is empty
        if phoneme_error:
            # Loop through the phoneme error
            for error in phoneme_error:
                correction_sentence += f"<li><span style=\"color:red;\">{error[0]}</span>: {error[1]}</li>"
        
            correction_sentence = '<ul>' + correction_sentence + '</ul>'

        # Define the HTML feedback
        feedback = ''

        # Mapping the final IELTS band to the feedback
        if final_ielts_band == 9:
            feedback = 'Outstanding pronunciation! Your speech is clear, confident, and fluent. Keep up the excellent work!'
        elif final_ielts_band == 8.5:
            feedback = 'Excellent pronunciation with very few minor errors. You are almost perfect—just refine your skills further!'
        elif final_ielts_band == 8:
            feedback = 'Great pronunciation! Your speech is clear and confident, with only minor areas for improvement.'
        elif final_ielts_band == 7.5:
            feedback = 'Very good pronunciation! You are doing well, but there are a few areas where you can improve clarity and consistency.'
        elif final_ielts_band == 7:
            feedback = 'Good pronunciation! Your speech is clear, but there is room for improvement in reducing errors and improving fluency.'
        elif final_ielts_band == 6.5:
            feedback = 'Decent pronunciation! You are on the right track, but focus on improving clarity and reducing minor errors.'
        elif final_ielts_band == 6:
            feedback = 'Your pronunciation is fair, but there are noticeable errors. Work on improving clarity and consistency.'
        elif final_ielts_band == 5.5:
            feedback = 'Your pronunciation needs improvement. Focus on reducing errors and improving the flow of your speech.'
        elif final_ielts_band == 5:
            feedback = 'Your pronunciation is understandable, but there are frequent errors. Practice speaking clearly and confidently.'
        elif final_ielts_band == 4.5:
            feedback = 'Your pronunciation is inconsistent, making it harder to understand. Focus on improving basic clarity and fluency.'
        elif final_ielts_band == 4:
            feedback = 'Your pronunciation has frequent errors that make understanding difficult. Work on basic pronunciation and clarity.'
        elif final_ielts_band == 3.5:
            feedback = 'Your pronunciation is poor, with significant errors. Focus on mastering basic sounds and improving fluency.'
        elif final_ielts_band == 3:
            feedback = 'Your pronunciation is very difficult to understand. Start with basic pronunciation exercises to improve clarity.'
        elif final_ielts_band == 2.5:
            feedback = 'Your pronunciation is almost unintelligible. Focus on learning basic sounds and practicing simple words.'
        elif final_ielts_band == 2:
            feedback = 'Your pronunciation is extremely unclear. Begin with foundational pronunciation practice to improve.'
        elif final_ielts_band == 1.5:
            feedback = 'Your pronunciation is nearly incomprehensible. Start with basic phonetics and simple word exercises.'
        else: 
            feedback = 'No attempt at pronunciation or completely unintelligible. Begin with learning basic sounds and words.'

        # Construct the HTML feedback
        html_feedback = ''

        # Add the original sentence
        html_feedback += f'<p><strong>Original Sentence:</strong></p>{original_sentence}'

        # Add the correction sentence if it exists
        if correction_sentence != '':
            html_feedback += f'<p><strong>Correction:</strong></p>{correction_sentence}'

        # Add the feedback
        html_feedback += f'<p><strong>Feedback:</strong></p><p>{feedback}</p>'

        # Return the HTML feedback
        return '<div>' + html_feedback + '</div>'

    # MARK: EvaluatePronunciation
    def evaluate_pronunciation(self, corpus_path: str, transcribe: str, words_timestamps: list) -> EvEvaluationModel:
        '''
        Evaluates the pronunciation of an audio file using the MFA tool and the confidence scores
        from word timestamps. The method takes the path to the corpus that contains the audio file
        type `wav` and a transcribe file type `txt` in the same directory. The method uses the MFA
        tool to align the audio file with the transcription and generate a TextGrid file. It then
        parses the TextGrid file to extract the phoneme. The method then calculates the average 
        confidence score from word timestamps. With those scores, it generates an EvEvaluationModel 
        that contain final IELTS band scores, readable feedback, and a dictionary of feedback 
        information. 
        '''
        try:
            # Check if transcribe is empty
            if transcribe == '':
                # Return the evaluation model
                return EvEvaluationModel(
                    ielts_band = 0,
                    readable_feedback = f'''
                        <p><strong>Feedback:</strong></p>
                        <p>Your transcription is empty. Please provide a valid transcription.</p>
                    ''',
                    feedback_information = {
                        'word_level_feedback': [],
                        'phoneme_count': 0,
                        'phoneme_error_count': 0,
                        'missing_phoneme_count': 0,
                        'word_count': 0,
                        'word_error_count': 0,
                        'missing_word_count': 0,
                        'mean_duration': 0,
                        'std_duration': 0,
                        'phoneme_ielts_band': 0,
                        'confidence_score': 0,
                        'confidence_ielts_band': 0,
                        'final_ielts_band': 0,
                    }
                )
            
            # Check if the corpus path exists
            if not os.path.exists(corpus_path):
                # Define the error message
                message = f'Corpus path {corpus_path} does not exist.'

                # Raise an exception with the error message
                raise EvServerException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get list of files in the corpus path
            files = os.listdir(corpus_path)

            # Check if the corpus path contains audio and transcription files
            if not any(file.endswith('.wav') for file in files) or not any(file.endswith('.txt') for file in files):
                # Define the error message
                message = f'Corpus path {corpus_path} must contain audio and transcription files.'

                # Raise an exception with the error message
                raise EvServerException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            try:
                # Run the MFA tool to align the audio file with the transcription
                subprocess.check_output([
                    self.tool,
                    self.task,
                    corpus_path,
                    self.dictionary,
                    self.acoustic_model,
                    corpus_path,
                    self.tags,
                ])

            except subprocess.CalledProcessError as e:
                # Define the error message
                message = f'Error running MFA tool: {e.output.decode()}'

                # Raise an exception with the error message
                raise EvServerException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get list of files in the corpus path
            files = os.listdir(corpus_path)

            # Check if the corpus path contains TextGrid files
            if not any(file.endswith(self.results_file_extension) for file in files):
                # Define the error message
                message = f'Corpus path {corpus_path} must contain TextGrid files after running MFA tool.'

                # Raise an exception with the error message
                raise EvServerException(
                    message = message,
                    information = {
                        'message': message,
                    }
                )
            
            # Get the path to the TextGrid file
            text_grid_path = os.path.join(corpus_path, [file for file in files if file.endswith(self.results_file_extension)][0])

            # Parse the TextGrid file
            text_grid = TextGrid.fromFile(text_grid_path)

            # Get the word and phoneme tiers
            phones_tier = next(text for text in text_grid.tiers if 'phone' in text.name.lower())
            words_tier = next(text for text in text_grid.tiers if 'word' in text.name.lower())

            # Define list of the feedback information from the TextGrid file
            word_level_feedback = []

            # Define count of the phonemes and words
            phoneme_count = 0
            phoneme_error_count = 0
            missing_phoneme_count = 0
            word_count = 0
            word_error_count = 0
            missing_word_count = 0

            # Define list of phoneme duration
            phoneme_durations = []

            # Loop through the words tier
            for word_interval in words_tier.intervals:
                # Get the word
                word = word_interval.mark.strip()

                # Check if the word is empty or contains unwanted characters
                if word == '' or word.lower() in ['<unk>', 'sil', 'sp']:
                    # Increment the missing word error count
                    missing_word_count += 1

                    # Skip the word
                    continue

                # Increment the word count
                word_count += 1

                # Define flag to know if the word have missing phonemes
                has_missing_phonemes = False

                # Define word level data
                word_data = {
                    'word': word,
                    'start': round(word_interval.minTime, 2),
                    'end': round(word_interval.maxTime, 2),
                    'phonemes': [],
                }

                # Loop through the phonemes tier
                for ph in phones_tier.intervals:
                    # Check if the phoneme is within the word interval
                    if ph.minTime >= word_interval.minTime and ph.maxTime <= word_interval.maxTime:
                        # Get the phoneme
                        ph_mark = ph.mark.strip()

                        # Check if the phoneme is empty or contains unwanted characters
                        if ph_mark == '' or ph_mark.lower() in ['sil', 'sp']:
                            # Increment the missing phoneme error count
                            missing_phoneme_count += 1

                            # Skip the phoneme
                            continue
                        
                        # Get the phoneme duration
                        duration = ph.maxTime - ph.minTime

                        # Define the status of the phoneme
                        status = 1

                        # Add the phoneme duration to the list
                        phoneme_durations.append(duration)

                        # Increment the phoneme count
                        phoneme_count += 1

                        # Check if phoneme duration is less than the threshold
                        if duration < self.phoneme_threshold:
                            # Increment the error count
                            phoneme_error_count += 1

                            # Set the status to 0 (not pronounced)
                            status = 0

                            # If not have missing phonemes
                            if not has_missing_phonemes:
                                # Set the flag to True
                                has_missing_phonemes = True

                        # Get the phoneme base
                        base = ''.join(filter(str.isalpha, ph_mark))

                        # Add the phoneme data to the word data
                        word_data['phonemes'].append({
                            'arpabert': ph_mark,
                            'ipa': self.arpabert_to_ipa.get(base.upper(), base.lower()),
                            'start': round(ph.minTime, 2),
                            'end': round(ph.maxTime, 2),
                            'status': status,
                        })

                    # Check if the phoneme minTime is less than the word interval minTime
                    elif ph.minTime < word_interval.minTime:
                        # Continue to the next phoneme
                        continue

                    # Check if the phoneme maxTime is greater than the word interval maxTime
                    elif ph.maxTime > word_interval.maxTime:
                        # Break the loop
                        break

                # Check if the word have missing phonemes
                if has_missing_phonemes:
                    # Increment the word error count
                    word_error_count += 1
                
                # Add the word level data to the list
                word_level_feedback.append(word_data)

            # Calculate the mean and standard deviation of the phoneme durations
            mean_duration = np.mean(phoneme_durations)
            std_duration = np.std(phoneme_durations)

            # Calculate the final IELTS band
            phoneme_ielts_band = self._map_pronounce_to_ielts_band(
                phoneme_count,
                phoneme_error_count,
                missing_phoneme_count,
            )

            # Calculate the average confidence score from word_timestamp
            avg_confidence = np.mean([float(word['confidence']) for word in words_timestamps if 'confidence' in word])

            # Calculate the confidence-based IELTS band
            confidence_ielts_band = self._map_confidence_to_ielts_band(avg_confidence)

            # Calculate the final IELTS band
            final_ielts_band = (
                (phoneme_ielts_band * 0.8) +
                (confidence_ielts_band * 0.2)
            )

            # Round the final IELTS band based on the IELTS band rules
            final_ielts_band = EvRoundedIELTSBand(final_ielts_band).rounded_band

            # Return the evaluation model
            return EvEvaluationModel(
                ielts_band = final_ielts_band,
                readable_feedback = self._generate_html_feedback(
                    word_level_feedback,
                    final_ielts_band,
                ),
                feedback_information = {
                    'word_level_feedback': word_level_feedback,
                    'phoneme_count': phoneme_count,
                    'phoneme_error_count': phoneme_error_count,
                    'missing_phoneme_count': missing_phoneme_count,
                    'word_count': word_count,
                    'word_error_count': word_error_count,
                    'missing_word_count': missing_word_count,
                    'mean_duration': mean_duration,
                    'std_duration': std_duration,
                    'phoneme_ielts_band': phoneme_ielts_band,
                    'confidence_score': avg_confidence,
                    'confidence_ielts_band': confidence_ielts_band,
                    'final_ielts_band': final_ielts_band,
                }
            )
        
        except EvServerException as error:
            # Raise the exception
            raise error
        
        except Exception as error:
            # Define the error message
            message = f'Error evaluating pronunciation: {str(error)}'

            # Raise an exception with the error message
            raise EvServerException(
                message = message,
                information = {
                    'message': message,
                }
            )

# MARK: PronunciationServiceInstance
# Create the pronunciation service instance
pronunciation_service = PronunciationService()
