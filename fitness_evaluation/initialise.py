from helpers import *


def initialise(Numberings, prev_schedule, M_List):
    numbering_count = len(Numberings)

    initial_zeroes = [0 for _ in range(numbering_count)]

    values = {
        'last_nr': [None for _ in range(numbering_count)],
        'total': initial_zeroes.copy(),
        'consecutive': initial_zeroes.copy(),

        # per_t is only used when evaluating current schedules, and since numberings for
        # those always start at 0, we can safely use the variable, for the i-th numbering, as:
        # per_t[i][the_numbering_the_event_falls_on] 
        'per_t': [[0 for _ in range(M_List[N]+1)] for N in range(numbering_count)],

        'penalty_min_consecutive': initial_zeroes.copy(),
        'penalty_max_consecutive': initial_zeroes.copy(),
        'penalty_min_between': initial_zeroes.copy(),
        'penalty_max_between': initial_zeroes.copy(),
        'penalty_max_total': initial_zeroes.copy(),
        'penalty_min_total': initial_zeroes.copy(),
        'penalty_max_per_t': [[0 for _ in range(M_List[N]+1)] for N in range(numbering_count)]
    }

    i = 0
    for numbering in Numberings:
        numbering_initialised = False

        last_nr = getMinNumbering(numbering)
        max_nr = getMaxNumbering(numbering)

        e = getLastEventTimeSlot(events_in_prev_schedule)
        while not numbering_initialised and e is not None: # running out of events not accounted for in (Burke)
            nr = numbering[e]

            if nr != None:
                new_nr = nr - max_nr - 1
                nr = new_nr # position of this step is erroneous in (Burke)
                lnr_less1 = last_nr - 1
                if nr == lnr_less1:
                    values['consecutive'][i] += 1
                elif nr < lnr_less1:
                    numbering_initialised = True

            # line below wrongly indented in (Burke), leading to an erroneous last_nr value==max_nr when no event
            # in the schedule matches a defined number in a numbering (in which case it should be undefined)
            last_nr = nr

            # get numbering of previous event in schedule
            e = getLastEventTimeSlot(events_in_prev_schedule[0:e])

        values['last_nr'][i] = last_nr
        i = i + 1

    return values


if __name__ == '__main__':
    from constraints import M_LIST, pN0, pN1, pN2
    import pprint as pp

    prev_numberings = [pN0, pN1, pN2]

    prev_personal_schedule1 = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 1,0,0, 1,0,0]
    prev_personal_schedule2 = [1,0,0, 0,0,1, 0,0,1, 0,0,0, 0,0,0, 0,0,0, 0,0,1]
    prev_solution = [prev_personal_schedule1, prev_personal_schedule2]

    A = initialise(prev_numberings, prev_personal_schedule1, M_LIST)
    # B = initialise(prev_numberings, prev_personal_schedule2, M_LIST)
    pp.pprint(A)
    # print(B)
