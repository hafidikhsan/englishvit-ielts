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
            buttonText: str,
            information: str = None,
        ):
        '''
        Initializes the EvIntroSectionModel with the given parameters.
        '''
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.buttonText = buttonText
        self.information = information

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'content': [item.to_dict() for item in self.content] if self.content else None,
            'button_text': self.buttonText,
            'information': self.information,
        }