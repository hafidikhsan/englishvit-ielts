# MARK: EvIntroSectionContentModel
class EvIntroSectionContentModel:
    '''
    EvIntroSectionContentModel is a base class for all introduction section content models. 
    This class provides a standard structure for introduction section content.
    '''
    def __init__(
            self, 
            type: int,
            title: str,
            label: str = None,
            subtitle: str = None,
            description: str = None,
            content: list = None,
            image_url: str = None,
        ):
        '''
        Initializes the EvIntroSectionContentModel with the given parameters.
        '''
        self.type = type
        self.title = title
        self.label = label
        self.subtitle = subtitle
        self.description = description
        self.content = content
        self.image_url = image_url

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'type': self.type,
            'title': self.title,
            'label': self.label,
            'subtitle': self.subtitle,
            'description': self.description,
            'content': [item.to_dict() for item in self.content],
            'image_url': self.image_url,
        }