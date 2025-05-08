from app.models.icon_text import EvIconTextModel

# EvIntroTestAudioContentModel
class EvIntroTestAudioContentModel:
    '''
    EvIntroTestAudioContentModel is a class that represents the audio content of an 
    introductory test. 
    '''
    def __init__(
            self, 
            title: str,
            mic_button: EvIconTextModel,
            speaker_button: EvIconTextModel,
            tips: EvIconTextModel,
        ):
        '''
        Initializes the EvIntroTestAudioContentModel with the given parameters.
        '''
        self.title = title
        self.mic_button = mic_button
        self.speaker_button = speaker_button
        self.tips = tips

    def to_dict(self):
        '''
        Converts the EvIntroTestAudioContentModel to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'title': self.title,
            'mic_button': self.mic_button.to_dict(),
            'speaker_button': self.speaker_button.to_dict(),
            'tips': self.tips.to_dict(),
        }