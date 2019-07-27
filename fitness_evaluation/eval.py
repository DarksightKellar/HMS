from initialise import *
from final_evaluation import *
from intermediate_evaluation import *


# Every personal schedule is evaluated separately
def evaluate(events_in_schedule, events_in_prev_schedule, Numberings):
    # initialise counter values
    values = initialise(Numberings, events_in_prev_schedule)
    cost = 0

    # get numbering of first event in `events_in_schedule`
    e = 0
    event_numbering = events_in_schedule[e]

    end_of_solution = False

    while not end_of_solution:
        # update all numbering counters with intermediate evaluation
        values = intermediate_evaluation(Numberings, event, values, last_nr)

        # get numbering of next event in planning period
        e = e + 1
        event_numbering = events_in_schedule[e]

    # perform final evaluation
    cost = final_evaluation(Numberings)
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
