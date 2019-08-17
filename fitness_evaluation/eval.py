from fitness_evaluation.initialise import *
from fitness_evaluation.final_evaluation import *
from fitness_evaluation.intermediate_evaluation import *
from fitness_evaluation.helpers import get_nth_event_numberings


# Every personal schedule is evaluated separately
def evaluate(schedule, prev_schedule, numberings, prev_numberings, M_LIST):
    # initialise counter values
    values = initialise(prev_numberings, prev_schedule, M_LIST)
    cost = 0

    # get numberings of first event in `events_in_schedule`
    event_n = 1
    event_numberings = get_nth_event_numberings(event_n, schedule, numberings)
    
    # Till end of solution
    while event_numberings is not None:
        # update all numbering counters with intermediate evaluation
        intermediate_evaluation(numberings, event_numberings, values)

        # get numbering of next event in planning period
        event_n += 1
        event_numberings = get_nth_event_numberings(event_n, schedule, numberings)

    # perform final evaluation
    final_evaluation(numberings, values)
    
    return values