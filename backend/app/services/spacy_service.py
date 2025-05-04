# Import dependency
import spacy
import datetime

# Import modules
from config import EvIELTSConfig
from app.utils.exception import EvException
from app.utils.logger import ev_logger

# MARK: SpacyService
class SpacyService:
    '''
    A class to manage all the spacy service. In this service will download
    and load the spacy model and perfome document analysis to split the
    document into sentences.
    '''
    # MARK: Init
    def __init__(self):
        # Class properties
        self.model_name = EvIELTSConfig.spacy_model_name
        self.model = None

        # Start download the model
        self._start_download_model(model_name = self.model_name)

    # MARK: StartDownloadModel
    def _start_download_model(self, model_name: str):
        try:
            ev_logger.info(f'Starting download {model_name} ...')

            # Try to load the ASR model
            self.model = spacy.load(model_name)

            ev_logger.info(f'Successfuly download {model_name} √')
        except Exception as error:
            ev_logger.info(f'Failed to download {model_name} ×')

    # MARK: CheckModel
    def check_model(self):
        return self.model is not None

    # MARK: HealthCheck
    def health_check(self):
        return {
            'model_ready': self.model is not None,
            'model_name': self.model_name,
            'model_type': 'Spacy',
            'tima_stamp': datetime.datetime.now()
        }
        
    # MARK: UpdateModel
    def update_model(self, model_name: str):
        # Update the model name propertied
        self.model_name = model_name

        # Start download new model
        self._start_download_model(model_name = model_name)

    # MARK: ProcessDocument
    def process_document(self, document: str):
        try:
            # If the model is empty
            if self.model is None:
                raise EvException(
                    f'Failed to process document: {document}',
                    status_code = 501,
                    information = {
                        'error': 'Model is empty'
                    }
                )

            # Process the document
            doc = self.model(document)

            # Return document sentences
            return doc

        except EvException as error:
            ev_logger.info(f'Failed to process document ×')

            # If the eror is EvException
            raise error

        except Exception as error:
            ev_logger.info(f'Failed to process document ×')

            # If something went wrong
            raise EvException(
                f'Failed to process document: {document}',
                status_code = 501,
                information = {
                    'error': str(error)
                }
            )
        
# MARK: SpacyService
# Create the Spacy service instance
spacy_service = SpacyService()