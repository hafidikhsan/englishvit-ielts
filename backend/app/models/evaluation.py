# MARK: EvEvaluationModel
class EvEvaluationModel:
    '''
    EvEvaluationModel is a base class for all evaluation process models. This class provides a
    standard structure for evaluation processes results, includes a final ielts band, readable
    feedback, and a dict of the feedback information. It also includes a method to convert the 
    response to a dictionary format.
    '''
    def __init__(self, ielts_band: float, readable_feedback: str, feedback_information: dict):
        '''
        Initializes the EvEvaluationModel with the given parameters.
        '''
        self.ielts_band = ielts_band
        self.readable_feedback = readable_feedback
        self.feedback_information = feedback_information

    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'ielts_band': self.ielts_band,
            'readable_feedback': self.readable_feedback,
            'feedback_information': self.feedback_information,
        }