def getMinNumbering(numbering):
    minimum = numbering[0]
    for n in numbering:
        if n is not None:
            if minimum is None:
                minimum = n
            elif n < minimum:
                minimum = n

    return minimum


def getMaxNumbering(numbering):
    maximum = numbering[0]
    for n in numbering:
        if n is not None:
            if maximum is None:
                maximum = n
            elif n > maximum:
                maximum = n

    return maximum


def getLastEventTimeSlot(schedule):
    last_index = None

    for i in range(len(schedule)):
        if schedule[i] != 0:
            last_index = i

    return last_index


def initialise(Numberings, events_in_prev_schedule, M_List):
        # per_t is only used when evaluating current schedules, and since numberings for
        # those always start at 0, we can safely use the variable, for the i-th numbering, as:
        # per_t[i][the_numbering_the_event_falls_on] 
    values = {
        'total': 0,
        'consecutive': 0,
        'per_t': [[0 for _ in range(M_List[N]+1)] for N in range(len(Numberings))],
        'last': 0,
        'penalty_min_consecutive': 1,
        'penalty_max_consecutive': 1,
        'penalty_min_between': 1,
        'penalty_max_between': 1,
        'N_last_nr': [0 for _ in range(len(Numberings))]
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
                    values['consecutive'] = values['consecutive'] + 1
                elif nr < lnr_less1:
                    numbering_initialised = True

                last_nr = nr

            # get numbering of previous event in schedule
            e = getLastEventTimeSlot(events_in_prev_schedule[0:e])

        values['N_last_nr'][i] = last_nr
        i = i + 1

    return values


if __name__ == '__main__':
    from constraints import M_LIST, pN0, pN1, pN2

    prev_numberings = [pN0, pN1, pN2]

    prev_personal_schedule1 = [1,0,0, 0,0,0, 0,0,0, 1,0,0, 0,0,0, 1,0,0, 1,0,0]
    prev_personal_schedule2 = [1,0,0, 0,0,1, 0,0,1, 0,0,0, 0,0,0, 0,0,0, 0,0,1]
    prev_solution = [prev_personal_schedule1, prev_personal_schedule2]

    A = initialise(prev_numberings, prev_personal_schedule1, M_LIST)
    B = initialise(prev_numberings, prev_personal_schedule2, M_LIST)

    print(A)
    # print(B)
