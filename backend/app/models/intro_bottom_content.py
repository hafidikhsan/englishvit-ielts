# MARK: EvIntroBottomContentModel
class EvIntroBottomContentModel:
    '''
    EvIntroBottomContentModel is a base class for all introduction bottom content models. 
    This class provides a standard structure for introduction bottom content.
    '''
    def __init__(
            self, 
            bottom_text: str,
            information,
        ):
        '''
        Initializes the EvIntroBottomContentModel with the given parameters.
        '''
        self.bottom_text = bottom_text
        self.information = information