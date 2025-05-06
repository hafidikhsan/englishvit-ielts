# MARK: Import
# Dependencies
import datetime

# Modules
from config import EvIELTSConfig

# MARK: EvResponseModel
class EvResponseModel:
    '''
    EvResponseModel is a base class for all response models. This class provides a 
    standard structure for responses, including a code, status, message, and data.
    It also includes a method to convert the response to a dictionary format.
    '''
    def __init__(self, code: int, status: str, message: str, data):
        '''
        Initializes the EvResponseModel with the given parameters.
        '''
        self.code = code
        self.status = status
        self.message = message
        self.data = data
        self.timestamp = datetime.datetime.now().isoformat()
        self.app_version = EvIELTSConfig.app_version
    
    def to_dict(self):
        '''
        Converts the response model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'meta': {
                'code': self.code,
                'status': self.status,
                'message': self.message,
                'timestamp': self.timestamp,
                'version': self.app_version,
            },
            'data': self.data,
        }