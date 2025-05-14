# MARK: Import 
# Dependency
import spacy
import datetime

# Modules
from config import EvIELTSConfig
from app.utils.exception import EvServerException
from app.utils.logger import ev_logger

# MARK: SpacyService
class SpacyService:
    '''
    A class to manage all the spacy service. In this service will download
    and load the spacy model and perform document analysis to split the
    document into sentences.
    '''
    # MARK: Properties
    def __init__(self):
        # Properties
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

            ev_logger.info(f'Successfully download {model_name} √')
        except Exception as error:
            ev_logger.info(f'Failed to download {model_name} x')

    # MARK: CheckModel
    def check_model(self):
        return self.model is not None

    # MARK: HealthCheck
    def health_check(self):
        return {
            'model_ready': self.model is not None,
            'model_name': self.model_name,
            'model_type': 'Spacy',
            'timestamp': datetime.datetime.now()
        }
        
    # MARK: UpdateModel
    def update_model(self, model_name: str):
        # Update the model name properties
        self.model_name = model_name

        # Start download new model
        self._start_download_model(model_name = model_name)

    # MARK: ProcessDocument
    def process_document(self, document: str):
        try:
            # If the model is empty
            if self.model is None:
                raise EvServerException(
                    f'Failed to process document: {document}',
                    information = {
                        'error': 'Model is empty'
                    }
                )

            # Process the document
            doc = self.model(document)

            # Return document sentences
            return doc

        except EvServerException as error:
            ev_logger.info(f'Failed to process document x')

            # If the error is EvServerException
            raise error

        except Exception as error:
            ev_logger.info(f'Failed to process document x')

            # If something went wrong
            raise EvServerException(
                f'Failed to process document: {document}',
                information = {
                    'error': str(error)
                }
            )
        
# MARK: SpacyServiceInstance
# Create the Spacy service instance
spacy_service = SpacyService()