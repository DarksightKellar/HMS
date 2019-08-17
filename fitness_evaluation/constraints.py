'''
These constraints are used in the numbering-based evaluation method.

TODO: These constraints should be encapsulated as a contract, to be applied per staff

'''

# For each numbering, the positive integer M representing the last number in the number sequence.
# This is what makes up the set {-M-1, −M, −M+1, ..., 0, 1, ..., M−1, M, U} to which a numbering maps
# this set is erroneously represented in (Burke)
M_LIST = [6, 6, 1]

from fitness_evaluation.numbering import Numbering
from helper_classes.constants import *

numbering_consecutive_days = Numbering.consecutive_days(N_DAYS, N_SHIFTS)
numbering_night_shifts = Numbering.consecutive_night_shifts(N_DAYS, N_SHIFTS)
numbering_weekends = Numbering.weekend(N_DAYS, N_SHIFTS)

# Number of different numberings
N_NUMBERINGS = 3

# The costs below are also per numbering

# upper, lower limits for number of events
MAX_TOTAL = [6 for _ in range(N_NUMBERINGS)]
MIN_TOTAL = [3 for _ in range(N_NUMBERINGS)]

# maximum, minimum number of consecutive events
MAX_CONSECUTIVE = [3 for _ in range(N_NUMBERINGS)]
MIN_CONSECUTIVE = [1 for _ in range(N_NUMBERINGS)]

# maximum, minimum gap between two non-consecutive events
MAX_BETWEEN = [3 for _ in range(N_NUMBERINGS)]
MIN_BETWEEN = [0 for _ in range(N_NUMBERINGS)]

# maximum, minimum number of events mappable to one time slot
MAX_PER_T = [[1 for _ in range(N+1)] for N in M_LIST]
MIN_PER_T = [[0 for _ in range(N+1)] for N in M_LIST]

# modify individual slots as required
# eg. MIN_PER_T[numering_i][nr] = 1
# Useful for day and/or shift on/off request constraints
