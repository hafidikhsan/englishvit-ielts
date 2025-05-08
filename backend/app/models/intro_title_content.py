# MARK: EvIntroTitleContentModel
class EvIntroTitleContentModel:
    '''
    EvIntroTitleContentModel is a base class for all introduction title content models. 
    This class provides a standard structure for introduction title content.
    '''
    def __init__(
            self, 
            title: str,
            subtitle: str,
            content: list,
        ):
        '''
        Initializes the EvIntroTitleContentModel with the given parameters.
        '''
        self.title = title
        self.subtitle = subtitle
        self.content = content

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'title': self.title,
            'sub_title': self.subtitle,
            'content': [item.to_dict() for item in self.content],
        }