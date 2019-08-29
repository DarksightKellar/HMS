from fitness_evaluation.costs import *

from fitness_evaluation.helpers import get_first_numbering
from fitness_evaluation.numbering import Numbering


def final_evaluation(Numberings, values):
    numbering_i = 0
    for _numbering in Numberings:
        _numbering: Numbering

        if values['total'][ numbering_i] == 1:
            values['consecutive'][numbering_i] = 1

        if values['total'][numbering_i] > _numbering.max_total:
            values['penalty_max_total'][numbering_i] += _numbering.cost_max_total * \
                (values['total'][numbering_i] - _numbering.max_total)

        if values['total'][numbering_i] < _numbering.min_total:
            values['penalty_min_total'][numbering_i] += _numbering.cost_min_total * \
                (_numbering.min_total - values['total'][numbering_i])

        if values['consecutive'][numbering_i] > _numbering.max_consecutive:
            values['penalty_max_consecutive'][numbering_i] += _numbering.cost_max_consecutive * \
                (values['consecutive'][numbering_i] - _numbering.max_consecutive)

        if values['consecutive'][numbering_i] < _numbering.min_consecutive:
            values['penalty_min_consecutive'][numbering_i] += _numbering.cost_min_consecutive * \
                (_numbering.min_consecutive - values['consecutive'][numbering_i])

        prev_t = None
        for t in _numbering.get_numberings():
            if t is None or t == prev_t:
                continue

            prev_t = t
            # hopefully MAX_PER_T is initialised as an array of coherent values before this point
            if values['per_t'][numbering_i][t] > _numbering.max_per_t[t]:
                values['penalty_max_per_t'][numbering_i][t] += _numbering.cost_max_pert * \
                    (values['per_t'][numbering_i][t] - _numbering.max_per_t[t])

            if values['per_t'][numbering_i][t] < _numbering.min_per_t[t]:
                values['penalty_min_per_t'][numbering_i][t] += _numbering.cost_min_pert * \
                    (_numbering.min_per_t[t] - values['per_t'][numbering_i][t])

        
        # Check how many unassigned numbers for this numbering remain,
        #  and use this to punish a max_between violation if needed
        last_nr = values['last_nr'][numbering_i]
        
        if last_nr != None:
            # The last_nr being None for this numbering at this point means that
            #  no event in this schedule was ever defined for this numbering.
            #  This should already have been appropriately punished in min_total logic.
            #  Here we care only about max_between, and since there's no relevant events 
            #  (last_nr has remained None throughout evaluation), then we forget it.
            max_numbering = _numbering.get_M()
            gap_to_end_of_period = _numbering.get_first_numbering() + max_numbering - last_nr

            if gap_to_end_of_period > _numbering.max_between:
                values['penalty_max_between'][numbering_i] += _numbering.cost_max_between * \
                    gap_to_end_of_period - _numbering.max_between

        numbering_i = numbering_i + 1
