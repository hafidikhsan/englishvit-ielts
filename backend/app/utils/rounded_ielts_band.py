# MARK: EvRoundedIELTSBand
class EvRoundedIELTSBand:
    '''
    Custom class to round float value to IELTS band.
    '''
    # MARK: Init
    def __init__(self, band: float):
        self.band = band
        self.rounded_band = round(band * 2) / 2.0