def get_nth_event_numberings(n, schedule, numberings):
    '''
    For all numberings in  `numberings`, 
    get the numbering of the `n`th event in `schedule`, in a list

    Returns `None` if there is no `n`th event
    '''
    events_encountered = 0
    event_index = -1
    event_numberings = []

    search_start_index = 0

    # Find index of event n
    while events_encountered < n:
        # e = [0,0,1,0,1]
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
        

    for numbering in numberings:
        event_numberings.append(numbering[event_index])

    return event_numberings

def getMinNumbering(numbering):
    '''
    Returns the minimum numbering that is defined
    '''
    minimum = numbering[0]
    for n in numbering:
        if n is not None and (minimum is None or n < minimum):
            minimum = n

    return minimum

def getMaxNumbering(numbering):
    '''
    Returns the maximum numbering that is defined
    '''
    maximum = numbering[0]
    for n in numbering:
        if n is not None and (maximum is None or n > maximum):
            maximum = n

    return maximum

def getLastEventTimeSlot(schedule):
    '''
    Returns the index of the last event in `schedule`
    '''
    last_index = None

    for i in range(len(schedule)):
        if schedule[i] != 0:
            last_index = i

    return last_index

def get_first_numbering(numbering):
    '''
    Returns the first non-None value in `numbering`
    '''
    for n in numbering:
        if n is not None:
            return n