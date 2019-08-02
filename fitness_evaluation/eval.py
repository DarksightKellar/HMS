from fitness_evaluation.initialise import *
from fitness_evaluation.final_evaluation import *
from fitness_evaluation.intermediate_evaluation import *
from fitness_evaluation.helpers import get_nth_event_numberings
from fitness_evaluation.constraints import M_LIST
    

# Every personal schedule is evaluated separately
def evaluate(schedule, prev_schedule, numberings, prev_numberings):
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

def nicelyprintresults(res):
    print('')
    pp.pprint(res)
    print('')

if __name__ == '__main__':
    import pprint as pp
    from constraints import \
        pN0, pN1, pN2, \
        N0, N1, N2, M_LIST
    
    prev_schedule = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 1,0,0, 1,0,0]

    schedule = [1,0,0, 1,0,0, 1,0,0, 0,1,0, 0,0,1, 0,0,0, 0,0,0]
    schedule2 = [1,0,0, 1,0,0, 1,0,0, 0,0,0, 0,0,0, 0,0,0, 1,0,0]

    numberings = [N0, N1, N2]
    prev_numberings = [pN0, pN1, pN2]
    
    nicelyprintresults(evaluate(schedule, prev_schedule, numberings, prev_numberings))
    nicelyprintresults(evaluate(schedule2, prev_schedule, numberings, prev_numberings))

    


