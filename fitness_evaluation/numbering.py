from math import ceil, floor
from fitness_evaluation.costs import *
from fitness_evaluation.constants import *


class Numbering():
    def __init__(self, 
        numbers,
        prev_numbers,
        n_days,
        n_shifts,

        cost_min_total = COST_MIN_TOTAL,
        cost_max_total = COST_MAX_TOTAL,
        cost_min_pert = COST_MIN_PERT,
        cost_max_pert = COST_MAX_PERT,
        cost_min_between = COST_MIN_BETWEEN,
        cost_max_between = COST_MAX_BETWEEN,
        cost_min_consecutive = COST_MIN_CONSECUTIVE,
        cost_max_consecutive = COST_MAX_CONSECUTIVE,
        
        min_total = MIN_TOTAL,
        max_total = MAX_TOTAL,
        min_consecutive = MIN_CONSECUTIVE,
        max_consecutive = MAX_CONSECUTIVE,
        min_between = MIN_BETWEEN,
        max_between = MAX_BETWEEN
    ):
        self.n = numbers
        self.p = prev_numbers
        self.n_days = n_days
        self.n_shifts = n_shifts
        self.n_allocations = n_days * n_shifts
        
        # Costs associated with this Numbering
        self.cost_min_total = cost_min_total
        self.cost_max_total = cost_max_total
        
        self.cost_min_pert = cost_min_pert
        self.cost_max_pert = cost_max_pert
        
        self.cost_min_between = cost_min_between
        self.cost_max_between = cost_max_between
        
        self.cost_min_consecutive = cost_min_consecutive
        self.cost_max_consecutive = cost_max_consecutive

        # upper, lower limits for number of events
        self.min_total = min_total
        self.max_total = max_total

        # maximum, minimum number of consecutive events
        self.min_consecutive = min_consecutive
        self.max_consecutive = max_consecutive

        # maximum, minimum gap between two non-consecutive events
        self.min_between = min_between
        self.max_between = max_between
        
        # minimum, maximum number of events mappable to each numbering
        M = self.get_M()
        self.min_per_t = [0 for _ in range(M+1)]
        self.max_per_t = [1 for _ in range(M+1)]

    def get_numberings(self):
        return self.n

    def get_previous(self):
        return self.p

    def get_numbering_at(self, time_slot):
        '''
        Get numbering at `time_slot`
        '''
        assert len(self.n) > time_slot
        return self.n[time_slot]

    def get_nth_event_numbering(self, n, schedule):
        '''
        Get the numbering of the `n`th event in `schedule`

        Returns `False` if there is no `n`th event
        '''
        events_encountered = 0
        event_index = -1

        search_start_index = 0

        # Find index of event n
        while events_encountered < n:
            try:
                list_to_search = schedule[search_start_index : ]
                event_index = list_to_search.index(1) + search_start_index

                # encountered an event
                events_encountered += 1
                if events_encountered == n:
                    break

                search_start_index = event_index + 1
            except ValueError as e:
                return False
            
        return self.n[event_index]

    def getMinNumbering(self):
        '''
        Returns the minimum numbering that is defined
        '''
        minimum = self.n[0]
        for n in self.n:
            if n is not None and (minimum is None or n < minimum):
                minimum = n

        return minimum

    def getMaxNumbering(self):
        '''
        Returns the maximum numbering that is defined
        '''
        maximum = self.n[0]
        for n in self.n:
            if n is not None and (maximum is None or n > maximum):
                maximum = n

        return maximum

    def get_M(self):
        '''
        Returns the positive integer M representing the last number in the number sequence.
        
        This is what makes up the set {-M-1, −M, −M+1, ..., 0, 1, ..., M−1, M, `None`}
        to which this numbering maps
        '''
        return self.getMaxNumbering()

    def set_max_per_t(self, nr, limit):
        # Useful for day and/or shift off request constraints (set to 0)
        self.max_per_t[nr] = limit

    def set_min_per_t(self, nr, limit):
        # Useful for day and/or shift on request constraints (set to 1)
        self.min_per_t[nr] = limit

    def get_first_numbering(self):
        '''
        Returns the first non-`None` value in this numering
        '''
        for n in self.n:
            if n is not None:
                return n
    
    # ################################################
    # FACTORY METHODS TO SET UP NUMBERING VALUES    #
    # ##############################################
    @classmethod
    def consecutive_days(self, n_days, n_shifts):
        '''
        Sets up this Numbering to check for consecutive days
        '''
        numbering = []
        prev_numbering = []
        for i in range(n_days * n_shifts):
            n = floor(i/n_shifts)
            numbering.append(n)
            prev_numbering.append((n+1) * -1)

        prev_numbering.reverse()

        return Numbering(numbering, prev_numbering, n_days, n_shifts)

    @classmethod
    def consecutive_night_shifts(self, n_days, n_shifts):
        '''
        Sets up this Numbering to check for consecutive night shifts
        '''
        numbering = []
        prev_numbering = []
        for i in range(n_days * n_shifts):
            n = floor(i/n_shifts)

            if (i+1) % n_shifts == 0:
                prev_numbering.append(None)
                numbering.append(n)
            elif (i+1) % n_shifts == 1:
                numbering.append(None)
                prev_numbering.append((n+1) * -1)
            else:
                prev_numbering.append(None)
                numbering.append(None)
                
        prev_numbering.reverse()

        return Numbering(numbering, prev_numbering, n_days, n_shifts)

    @classmethod
    def morning_after_night(self, n_days, n_shifts):
        '''
        Sets up this Numbering to check for a morning assignment
        after a night shift assignment
        '''
        numbering = [-1]
        prev_numbering = [-1]
        for i in range(1, n_days * n_shifts):
            n = floor(i/n_shifts)
            
            if (i+1) % n_shifts == 0:
                numbering.append(n)
                prev_numbering.append(-1 * (n+2))
            elif (i+1) % n_shifts == 1:
                numbering.append(n-1)
                prev_numbering.append(-1 * (n+1))
            else: 
                numbering.append(None)
                prev_numbering.append(None)
                
        prev_numbering.reverse()

        return Numbering(numbering, prev_numbering, n_days, n_shifts)


    @classmethod
    def weekend(self, n_days, n_shifts):
        '''
        Sets up this Numbering to check for weekend assignments
        '''
        numbering = []
        prev_numbering = []

        number = 0
        
        # prev_number starts (counting backward) from -2 instead of -1 because the next number in the current
        # numbering would be 0, but logically there's actually a gap between the two events, if they do occur
        # on those numbers, so we don't want the algorithm to treat them as consecutive
        # (but what if we're also looking at min/max consecutive weekends? ... sth for Future Kelvin to ponder)
        # (Maybe that's just be another numbering, albeit similar to this...)
        prev_number = -2
        for i in range(n_days * n_shifts):
            n = floor(i/n_shifts)

            is_weekend = False
            prev_is_weekend = False
            if (n+1) % 7 == 0 or (n+1) % 7 == 6: # a sunday or saturday
                is_weekend = True

            
            if (n+1) % 7 == 1 or (n+1) % 7 == 2: 
                # a sunday or saturday (counting from behind, since prev_numbering will be reversed)
                prev_is_weekend = True

            if is_weekend:
                numbering.append(number)
                number += 1 if (i+1)%n_shifts == 0 else 0
            else:
                numbering.append(None)

            if prev_is_weekend:
                prev_numbering.append(prev_number)
                prev_number -= 1 if (i+1)%n_shifts == 0 else 0
            else:
                prev_numbering.append(None)

        prev_numbering.reverse()

        return Numbering(numbering, prev_numbering, n_days, n_shifts)

if __name__ == '__main__':
    numbering = Numbering.weekend(14, 3)
    print(numbering.get_previous())
    print(numbering.get())