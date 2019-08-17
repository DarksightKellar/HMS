from math import ceil, floor


class Numbering():
    def __init__(self, numbers, prev_numbers, n_days, n_shifts):
        self.n = numbers
        self.p = prev_numbers
        self.n_allocations = n_days * n_shifts
        self.n_days = n_days
        self.n_shifts = n_shifts

    def get(self):
        return self.n

    def get_previous(self):
        return self.p

    def get_numbering(self, time_slot):
        '''
        Get numbering at `time_slot`
        '''
        assert len(self.n) > time_slot
        return self.n[time_slot]

    def get_nth_event_numbering(self, n, schedule):
        '''
        Get the numbering of the `n`th event in `schedule`

        Returns `None` if there is no `n`th event
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
                return None
            
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
    def weekend(self, n_days, n_shifts):
        '''
        Sets up this Numbering to check for weekend assignments
        '''
        numbering = []
        prev_numbering = []

        number = 0
        prev_number = -1
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