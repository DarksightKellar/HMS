from initialise import *
from final_evaluation import *
from intermediate_evaluation import *


def get_nth_event_numberings(n, events, numberings):
    '''
    For all numberings in  `numberings`, 
    get the numbering of the `n`th event in `events`, in a list

    Returns `None` if there is no `n`th event
    '''
    events_encountered = 0
    event_index = 0
    event_numberings = []

    # Find index of event n
    while events_encountered < n:
        while events[event_index] is not 1:
            event_index += 1

            # if event_index reaches event list size, we've run outta events
            if event_index == len(events):
                return None

        events_encountered += 1

    for numbering in numberings:
        event_numberings.append(numbering[event_index])

    return event_numberings
    

# Every personal schedule is evaluated separately
def evaluate(events_in_schedule, events_in_prev_schedule, numberings, prev_numberings, M_LIST):
    # initialise counter values
    values = initialise(prev_numberings, events_in_prev_schedule, M_LIST)
    cost = 0

    # get numberings of first event in `events_in_schedule`
    event_n = 1
    event_numberings = get_nth_event_numberings(event_n, events_in_schedule, numberings)

    end_of_solution = False

    while not end_of_solution:
        # update all numbering counters with intermediate evaluation
        values = intermediate_evaluation(numberings, event, values, last_nr)

        # get numbering of next event in planning period
        event_n += 1
        event_numberings = get_nth_event_numberings(event_n, events_in_schedule, numberings)

    # perform final evaluation
    cost = final_evaluation(numberings)
    return [cost, values]

if __name__ == '__main__':
    from constraints import \
        pN0, pN1, pN2, \
        N0, N1, N2, M_LIST
    
    events = [1,0,0, 1,0,0, 0,1,0, 0,1,0, 0,0,1, 0,0,0, 0,0,0]
    prev_events = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 1,0,0, 1,0,0]

    numberings = [N0, N1, N2]
    prev_numberings = [pN0, pN1, pN2]

    evaluate(events, prev_events, numberings, prev_numberings, M_LIST)
