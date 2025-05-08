# MARK: EvIntroTitleContentModel
class EvIntroTitleContentModel:
    '''
    EvIntroTitleContentModel is a base class for all introduction title content models. 
    This class provides a standard structure for introduction title content.
    '''
    def __init__(
            self, 
            title: str,
            sub_title: str,
            content: list,
        ):
        '''
        Initializes the EvIntroTitleContentModel with the given parameters.
        '''
        self.title = title
        self.sub_title = sub_title
        self.content = content