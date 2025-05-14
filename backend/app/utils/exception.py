# MARK: EvException
class EvException(Exception):
    '''
    Custom exception class raised by the app.
    '''
    # MARK: Properties
    def __init__(self, message: str, status_code: int = 500, information: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.information = information or {}

# MARK: EvServerException
class EvServerException(EvException):
    '''
    Custom exception class for server errors.
    '''
    # MARK: Properties
    def __init__(self, message: str, information: dict = None):
        super().__init__(message, 500, information)

# MARK: EvClientException
class EvClientException(EvException):
    '''
    Custom exception class for client errors.
    '''
    # MARK: Properties
    def __init__(self, message: str, information: dict = None):
        super().__init__(message, 400, information)

# MARK: EvAPIException
class EvAPIException(EvException):
    '''
    Custom exception class for API errors.
    '''
    # MARK: Properties
    def __init__(self, message: str, information: dict = None):
        super().__init__(message, 510, information)