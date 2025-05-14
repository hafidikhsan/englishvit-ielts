# MARK: EvIntroSpeakingIntroductionListModel
class EvIntroSpeakingIntroductionListModel:
    '''
    EvIntroSpeakingIntroductionListModel is a base class for all introduction speaking introduction list models. 
    This class provides a standard structure for introduction speaking introduction list.
    '''
    def __init__(
            self, 
            title: str,
            image_url: str = None,
        ):
        '''
        Initializes the EvIntroSpeakingIntroductionListModel with the given parameters.
        '''
        self.title = title
        self.image_url = image_url

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'title': self.title,
            'image_url': self.image_url,
        }