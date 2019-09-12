from fitness_evaluation.constants import *
from fitness_evaluation.numbering import Numbering
from helper_classes.constants import N_DAYS, N_SHIFTS

class Contract():
    def __init__(self, 
            limit_total=[MIN_TOTAL, MAX_TOTAL], 
            limit_consecutive=[MIN_CONSECUTIVE, MAX_CONSECUTIVE], 
            limit_between=[MIN_BETWEEN, MAX_BETWEEN],
            n_days=N_DAYS,
            n_shifts=N_SHIFTS,
            numberings=None
        ):

        self.min_total = limit_total[0]
        self.max_total = limit_total[1]

        self.min_consecutive = limit_consecutive[0]
        self.max_consecutive = limit_consecutive[1]

        self.min_between = limit_between[0]
        self.max_between = limit_between[1]

        if numberings is None:
            numberings = [
                Numbering.consecutive_days(n_days, n_shifts),
                Numbering.morning_after_night(n_days, n_shifts),
                Numbering.consecutive_night_shifts(n_days, n_shifts),
                Numbering.weekend(n_days, n_shifts)
            ]
            
        self.numberings = numberings
        self.n_numberings = len(numberings)