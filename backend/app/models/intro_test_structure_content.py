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
            sub_title: EvIconTextModel,
        ):
        '''
        Initializes the EvIntroTestStructureContentModel with the given parameters.
        '''
        self.label = label
        self.title = title
        self.content = content
        self.sub_title = sub_title