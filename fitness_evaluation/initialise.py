import pprint as pp
from fitness_evaluation.helpers import *
from fitness_evaluation.numbering import Numbering


def initialise(Numberings, prev_schedule):
    numbering_count = len(Numberings)

    initial_zeroes = [0 for _ in range(numbering_count)]
    M_List = [n.get_M() for n in Numberings]

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
    prev_numberings = [n.get_previous() for n in Numberings]
    for numbering in prev_numberings:
        numbering_initialised = False

        last_nr = getMinNumbering(numbering)
        max_nr = getMaxNumbering(numbering)

        e = getLastEventTimeSlot(prev_schedule)

        if e is None:
            # No event in prev_schedule, vamoose
            continue
        
        if numbering[e] is not None:
            # Since we've found an event at the end of prev_schedule 
            # that is defined on this numbering,
            # increment consecutive to prepare to count
            # potential extra consecutive events if any.
            # Even if no extra consecutive event is found,
            # this should still remain 1, as at least one event
            # for this numbering exists
            # (Grossly overlooked, yet assumed, in Burke. GADDAMIT!!!)
            values['consecutive'][i] += 1
        
        last_event_nr = numbering[e]
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
            e = getLastEventTimeSlot(prev_schedule[0:e])

        values['last_nr'][i] = last_event_nr
        i = i + 1

    # print('initial values')
    # pp.pprint(values)
    return values
