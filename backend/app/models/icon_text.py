# MARK: EvIconTextModel
class EvIconTextModel:
    '''
    EvIconTextModel is a base class for all icon text models. This class provides a standard structure for icon text.
    '''
    def __init__(
            self, 
            icon_url: str,
            text: str,
        ):
        '''
        Initializes the EvIconTextModel with the given parameters.
        '''
        self.icon_url = icon_url
        self.text = text