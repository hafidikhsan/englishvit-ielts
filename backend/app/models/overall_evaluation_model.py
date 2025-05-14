# MARK: EvOverallEvaluationModel
class EvOverallEvaluationModel:
    '''
    EvOverallEvaluationModel is a model class that provides information about the overall evaluation.
    It includes the final IELTS band, overall feedback, and specific feedback information based on the
    IELTS evaluation criteria.
    '''
    # MARK: Properties
    def __init__(
            self, 
            overall_band: float, 
            overall_feedback: str,
            fluency_band: float,
            fluency_feedback: str,
            lexical_band: float,
            lexical_feedback: str,
            grammar_band: float,
            grammar_feedback: str,
            pronunciation_band: float,
            pronunciation_feedback: str,
        ):
        '''
        Initializes the EvOverallEvaluationModel with the given parameters.
        '''
        self.overall_band = overall_band
        self.overall_feedback = overall_feedback
        self.fluency_band = fluency_band
        self.fluency_feedback = fluency_feedback
        self.lexical_band = lexical_band
        self.lexical_feedback = lexical_feedback
        self.grammar_band = grammar_band
        self.grammar_feedback = grammar_feedback
        self.pronunciation_band = pronunciation_band
        self.pronunciation_feedback = pronunciation_feedback

    # MARK: ToDict
    def to_dict(self):
        '''
        Converts the evaluation model to a dictionary format.
        This method is useful for returning JSON responses in Flask.
        '''
        return {
            'overall_band': self.overall_band,
            'overall_feedback': self.overall_feedback,
            'fluency_band': self.fluency_band,
            'fluency_feedback': self.fluency_feedback,
            'lexical_band': self.lexical_band,
            'lexical_feedback': self.lexical_feedback,
            'grammar_band': self.grammar_band,
            'grammar_feedback': self.grammar_feedback,
            'pronunciation_band': self.pronunciation_band,
            'pronunciation_feedback': self.pronunciation_feedback,
        }