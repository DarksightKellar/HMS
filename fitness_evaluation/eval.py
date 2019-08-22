from fitness_evaluation.initialise import *
from fitness_evaluation.final_evaluation import *
from fitness_evaluation.intermediate_evaluation import *
from fitness_evaluation.helpers import get_nth_event_numberings


# Every personal schedule is evaluated separately
def evaluate(schedule, prev_schedule, numberings):
    # initialise counter values
    values = initialise(numberings, prev_schedule)
    cost = 0

    # Till we run out of events to check, run intermediate evaluation on each event in schedule
    event_n = 1
    while True:
        # update all numbering counters with intermediate evaluation
        if intermediate_evaluation(numberings, values, schedule, event_n) == 'no event':
            break

        event_n += 1

    # perform final evaluation
    final_evaluation(numberings, values)
    
    return values