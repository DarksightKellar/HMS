'''
These constraints are used in the numbering-based evaluation method.

TODO: These constraints should be encapsulated as a contract, to be applied per staff

'''

# TODO: Write functions that can construct these numberings dynamically, given number of days in
# scheduling period and number of shifts per day. Also generates the corresponding M_LIST
pN0 = [-7,-7,-7, -6,-6,-6, -5,-5,-5, -4,-4,-4, -3,-3,-3, -2,-2,-2, -1,-1,-1]  
pN1 = [None,None,-7, None,None,-6, None,None,-5, None,None,-4, None,None,-3, None,None,-2, None,None,-1]

# pN2 starts (counting backward) from -2 instead of -1 because the next number in the current
# numbering N3 is 0, but logically there's actually a gap between the two events, if they do occur
# on those numbers, so we don't want the algorithm to treat them as consecutive
# (but what if we're also looking at min/max consecutive weekends? ... sth for Future Kelvin to ponder)
# (Maybe that's just be another numbering, albeit similar to this...)
pN2 = [None,None,None, None,None,None, None,None,None, None,None,None, None,None,None, -3,-3,-3, -2,-2,-2]

# prev_events = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 1,0,0, 1,0,0]
# events = [1,0,0, 1,0,0, 0,1,0, 0,1,0, 0,0,1, 0,0,0, 0,0,0]
N0 = [0,0,0, 1,1,1, 2,2,2, 3,3,3, 4,4,4, 5,5,5, 6,6,6]  
N1 = [None,None,0, None,None,1, None,None,2, None,None,3, None,None,4, None,None,5, None,None,6]  
N2 = [None,None,None, None,None,None, None,None,None, None,None,None, None,None,None, 0,0,0, 1,1,1]
 
# For each numbering, the positive integer M representing the last number in the number sequence.
# This is what makes up the set {-M-1, −M, −M+1, ..., 0, 1, ..., M−1, M, U} to which a numbering maps
# this set is erroneously represented in (Burke)
M_LIST = [6, 6, 1]

'''
The following are constraints used and their numberings for them (for a 30-day period; 3 shifts per day):

- [0, 1, 2, ..., 87, 88, 89]
  - Max, Min number of assignments (set max_total, min_total to desired values)
    NB: No numbering is actually used for this. during evaluation, each time
        an event is encountered, total is simply incremented, then checked against 
        max_total and min_total at the end of the day

- [0, 0, 0, ..., 29, 29, 29]
  - Max, Min number of consecutive working days; (set max_, min_consecutive to desired values)
  - Max, Min number of consecutive free days
  - Single Assignment per day: [same as above, max_per_t[:] is set to 1]

- [None, None, 0, ..., None, None, 29]
    - Max, min number of consecutive night shifts

- [None,None,None, ..., 29]
'''
# Number of different numberings
N_NUMBERINGS = 3

# The costs below are also per numbering

# upper, lower limits for number of events
MAX_TOTAL = [1 for _ in range(N_NUMBERINGS)]
MIN_TOTAL = [1 for _ in range(N_NUMBERINGS)]

# maximum, minimum number of consecutive events
MAX_CONSECUTIVE = [2 for _ in range(N_NUMBERINGS)]
MIN_CONSECUTIVE = [1 for _ in range(N_NUMBERINGS)]

# maximum, minimum gap between two non-consecutive events
MAX_BETWEEN = [1 for _ in range(N_NUMBERINGS)]
MIN_BETWEEN = [0 for _ in range(N_NUMBERINGS)]

# maximum, minimum number of events mappable to one time slot
MAX_PER_T = [[1 for _ in range(N+1)] for N in M_LIST]
MIN_PER_T = [[0 for _ in range(N+1)] for N in M_LIST]

# modify individual slots as required
# eg. MIN_PER_T[numering_i][nr] = 1
# Useful for day and/or shift on/off request constraints
