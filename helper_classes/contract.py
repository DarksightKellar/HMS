from fitness_evaluation.constants import *
from fitness_evaluation.numbering import Numbering
from helper_classes.constants import N_DAYS, N_SHIFTS

class Contract():
    def __init__(self, 
            limit_total=[MIN_TOTAL, MAX_TOTAL], 
            limit_consecutive=[MIN_CONSECUTIVE, MAX_CONSECUTIVE], 
            limit_between=[MIN_BETWEEN, MAX_BETWEEN],
            numberings=[
                Numbering.consecutive_days(N_DAYS, N_SHIFTS),
                Numbering.consecutive_night_shifts(N_DAYS, N_SHIFTS),
                Numbering.weekend(N_DAYS, N_SHIFTS)
            ]
        ):

        self.min_total = limit_total[0]
        self.max_total = limit_total[1]

        self.min_consecutive = limit_consecutive[0]
        self.max_consecutive = limit_consecutive[1]

        self.min_between = limit_between[0]
        self.max_between = limit_between[1]

        self.numberings = numberings
        self.n_numberings = len(numberings)