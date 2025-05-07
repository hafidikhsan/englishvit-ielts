# Import dependencies
import datetime
import whisper_timestamped
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Import modules
from config import EvIELTSConfig
from app.utils.exception import EvException
from app.utils.logger import ev_logger

# MARK: ASRService
class ASRService:
    '''
    A class to manage all the ASR service. In this service will download
    and load the ASR model. The ASR model I use custom fine tuned whisper
    model.
    '''
    # MARK: Init
    def __init__(self):
        # Class properties
        self.model_name = EvIELTSConfig.asr_model_name
        self.model = None

        # Start download the model
        self._start_download_model(model_name = self.model_name)

    # MARK: StartDownloadModel
    def _start_download_model(self, model_name: str):
        try:
            ev_logger.info(f'Starting download {model_name} ...')

            # Try to load the ASR model
            self.model = whisper_timestamped.load_model(
                model_name,
                device = 'cpu',
            )

            ev_logger.info(f'Successfuly download {model_name} √')
        except Exception as error:
            ev_logger.info(f'Failed to download {model_name} ×')
            ev_logger.info(f'Error: {error}')

    # MARK: CheckModel
    def check_model(self):
        return self.model is not None

    # MARK: HealthCheck
    def health_check(self):
        return {
            'model_ready': self.model is not None,
            'model_name': self.model_name,
            'model_type': 'Whisper',
            'tima_stamp': datetime.datetime.now()
        }

    # MARK: UpdateModel
    def update_model(self, model_name: str):
        # Update the model name propertied
        self.model_name = model_name

        # Start download new model
        self._start_download_model(model_name = model_name)

    # MARK: ProcessAudio
    def process_audio(self, audio_file_path: str):
        try:
            # If the model is empty
            if self.model is None:
                raise EvException(
                    f'Failed to process audio: {audio_file_path}',
                    status_code = 501,
                    information = {
                        'error': 'Model is empty'
                    }
                )

            # Define whisper audio path
            whisper_audio_file_path = whisper_timestamped.load_audio(
                audio_file_path
            )

            # Transcribe the audio
            result = whisper_timestamped.transcribe(
                self.model,
                whisper_audio_file_path,
                language = 'en',
                detect_disfluencies = True,
            )

            # Variable to save the words transcribe
            words = []

            # Loop through the transcribe segments
            for segment in result['segments']:
                # Loop through the segment words
                for word in segment['words']:
                    # Get the text information
                    text = word['text']

                    if '[' in text and ']' in text:
                        # If text is special character, don't add to the words list
                        continue

                    # Add to the words list a word model that contain text, start, end, and confidance
                    words.append(word)

            # Get the string of the word transcribe
            transcribe = ' '.join([word['text'] for word in words])

            # List of word with the tag
            word_with_tag = []

            # Loop through the word list
            for word in words:
                # Word tokenize
                tokens = word_tokenize(word['text'])

                # Tagging the token
                pos_tags = pos_tag(tokens)

                # Get start, end, confidence data
                start = word['start']
                end = word['end']
                confidence = word['confidence']

                # Loop throught the pos tags
                for pos_tag_data in pos_tags:
                    # Add to the word with tag list
                    word_with_tag.append({
                        'text': pos_tag_data[0],
                        'start': start,
                        'end': end,
                        'confidence': confidence,
                        'tag': pos_tag_data[1],
                    })

            # Return the transcribe and the words time stampt
            return (transcribe, word_with_tag)

        except EvException as error:
            # If the eror is EvException
            raise error

        except Exception as error:
            ev_logger.info(f'Failed to process audio {audio_file_path} ×')

            # If something went wrong
            raise EvException(
                f'Failed to process audio: {audio_file_path}',
                status_code = 501,
                information = {
                    'error': str(error)
                }
            )
        
# MARK: ASRService
# Create the ASR service instance
asr_service = ASRService()