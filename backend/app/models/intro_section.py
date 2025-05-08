# MARK: EvIntroSectionModel
class EvIntroSectionModel:
    '''
    EvIntroSectionModel is a base class for all introduction section models. This class provides a
    standard structure for introduction sections.
    '''
    def __init__(
            self, 
            title: str,
            subtitle: str,
            content: list,
        ):
        '''
        Initializes the EvIntroSectionModel with the given parameters.
        '''
        self.title = title
        self.subtitle = subtitle
        self.content = content