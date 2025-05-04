# MARK: EvException
class EvException(Exception):
    '''
    Custom exception class raised by the app.
    '''
    # MARK: Init
    def __init__(self, message: str, status_code: int = 500, information: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.information = information or {}