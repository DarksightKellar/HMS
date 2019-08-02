from fitness_evaluation.constraints import *
from fitness_evaluation.costs import *

from fitness_evaluation.helpers import get_first_numbering


def final_evaluation(Numberings, values):
    numbering_i = 0
    for numbering in Numberings:
        if values['total'][ numbering_i] == 1:
            values['consecutive'][numbering_i] = 1

        if values['total'][numbering_i] > MAX_TOTAL[numbering_i]:
            values['penalty_max_total'][numbering_i] += COST_MAX_TOTAL[numbering_i] * \
                (values['total'][numbering_i] - MAX_TOTAL[numbering_i])

        if values['total'][numbering_i] < MIN_TOTAL[numbering_i]:
            values['penalty_min_total'][numbering_i] += COST_MIN_TOTAL[numbering_i] * \
                (MIN_TOTAL[numbering_i] - values['total'][numbering_i])

        if values['consecutive'][numbering_i] > MAX_CONSECUTIVE[numbering_i]:
            values['penalty_max_consecutive'][numbering_i] += COST_MAX_CONSECUTIVE[numbering_i] * \
                (values['consecutive'][numbering_i] - MAX_CONSECUTIVE[numbering_i])

        if values['consecutive'][numbering_i] < MIN_CONSECUTIVE[numbering_i]:
            values['penalty_min_consecutive'][numbering_i] += COST_MIN_CONSECUTIVE[numbering_i] * \
                (MIN_CONSECUTIVE[numbering_i] - values['consecutive'][numbering_i])

        prev_t = None
        for t in numbering:
            if t is None or t == prev_t:
                continue

            prev_t = t
            # hopefully MAX_PER_T is initialised as an array of coherent values before this point
            if values['per_t'][numbering_i][t] > MAX_PER_T[numbering_i][t]:
                values['penalty_max_per_t'][numbering_i][t] += COST_MAX_PERT[numbering_i] * \
                    (values['per_t'][numbering_i][t] - MAX_PER_T[numbering_i][t])

            if values['per_t'][numbering_i][t] < MIN_PER_T[numbering_i][t]:
                values['penalty_min_per_t'][numbering_i][t] += COST_MIN_PERT[numbering_i] * \
                    (MIN_PER_T[numbering_i][t] - values['per_t'][numbering_i][t])

        
        # Check how many unassigned numbers for this numbering remain,
        #  and use this to punish a max_between violation if needed
        last_nr = values['last_nr'][numbering_i]
        
        if last_nr != None:
            # The last_nr being None for this numbering at this point means that
            #  no event in this schedule was ever defined for this numbering.
            #  This should already have been appropriately punished in min_total logic.
            #  Here we care only about max_between, and since there's no relevant events 
            #  (last_nr has remained None throughout evaluation), then we forget it.
            max_numbering = M_LIST[numbering_i]
            gap_to_end_of_period = get_first_numbering(numbering) + max_numbering - last_nr

            if gap_to_end_of_period > MAX_BETWEEN[numbering_i]:
                values['penalty_max_between'][numbering_i] += COST_MAX_BETWEEN[numbering_i] * \
                    gap_to_end_of_period - MAX_BETWEEN[numbering_i]

        numbering_i = numbering_i + 1
