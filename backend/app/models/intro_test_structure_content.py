from app.models.icon_text import EvIconTextModel

# MARK: EvIntroTestStructureContentModel
class EvIntroTestStructureContentModel:
    '''
    EvIntroTestStructureContentModel is a base class for all introduction test structure content models.
    This class provides a standard structure for introduction test structure content.
    '''
    def __init__(
            self, 
            label: str,
            title: str,
            content: str,
            subtitle: EvIconTextModel,
        ):
        '''
        Initializes the EvIntroTestStructureContentModel with the given parameters.
        '''
        self.label = label
        self.title = title
        self.content = content
        self.subtitle = subtitle

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'label': self.label,
            'title': self.title,
            'content': self.content,
            'sub_title': self.subtitle.to_dict(),
        }