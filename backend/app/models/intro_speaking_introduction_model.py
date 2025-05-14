# MARK: EvIntroSpeakingIntroductionModel
class EvIntroSpeakingIntroductionModel:
    '''
    EvIntroSpeakingIntroductionModel is a base class for all introduction speaking introduction models. 
    This class provides a standard structure for introduction speaking introduction.
    '''
    def __init__(
            self, 
            title: str,
            label: str,
            descriptions: list,
            instructions: list,
            outroMessage: str,
            tips = None, 
            nextPart: str = None,
        ):
        '''
        Initializes the EvIntroSpeakingIntroductionModel with the given parameters.
        '''
        self.title = title
        self.label = label
        self.descriptions = descriptions
        self.instructions = instructions
        self.outroMessage = outroMessage
        self.tips = tips
        self.nextPart = nextPart

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'title': self.title,
            'label': self.label,
            'descriptions': self.descriptions,
            'instructions': [item.to_dict() for item in self.instructions],
            'outro_message': self.outroMessage,
            'tips': self.tips.to_dict() if self.tips else None,
            'next_part': self.nextPart if self.nextPart else None,
        }