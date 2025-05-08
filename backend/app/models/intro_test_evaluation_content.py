# MARK: EvIntroTestEvaluationContentModel
class EvIntroTestEvaluationContentModel:
    '''
    EvIntroTestEvaluationContentModel is a base class for all introduction test evaluation content models. 
    This class provides a standard structure for introduction test evaluation content.
    '''
    def __init__(
            self, 
            title: str,
            subtitle: str,
            content: list,
            icon_url: str,
        ):
        '''
        Initializes the EvIntroTestEvaluationContentModel with the given parameters.
        '''
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.icon_url = icon_url

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'content': [item.to_dict() for item in self.content],
            'icon_url': self.icon_url,
        }