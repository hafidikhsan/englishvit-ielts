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