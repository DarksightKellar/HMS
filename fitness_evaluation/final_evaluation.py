from constraints import *
from costs import *


def final_evaluation(Numberings, values):
    for numbering in Numberings:
        if values['total'] > MAX_TOTAL:
            values['penalty_max_total'] = values['penalty_max_total'] + \
                COST_MAX_TOTAL * (values['total'] - MAX_TOTAL)

        if values['total'] < MIN_TOTAL:
            values['penalty_min_total'] = values['penalty_min_total'] + \
                COST_MIN_TOTAL * (MIN_TOTAL - values['total'])

        if values['consecutive'] > MAX_CONSECUTIVE:
            values['penalty_max_consecutive'] = values['penalty_max_consecutive'] + \
                COST_MAX_CONSECUTIVE * \
                (values['consecutive'] - MAX_CONSECUTIVE)

        if values['consecutive'] < MIN_CONSECUTIVE:
            values['penalty_min_consecutive'] = values['penalty_min_consecutive'] + \
                COST_MIN_CONSECUTIVE * \
                (MIN_CONSECUTIVE - values['consecutive'])

        for t in numbering:
            # hopefully MAX_PER_T is initialised as an array of coherent values before this point
            if per_t[t] > MAX_PER_T[t]:
                values['penalty_max_per_t'] = values['penalty_max_per_t'] + \
                    COST_MAX_PERT * (per_t[t] - MAX_PER_T[t])

            if per_t[t] < MIN_PER_T[t]:
                values['penalty_min_per_t'] = values['penalty_min_per_t'] + \
                    COST_MIN_PERT * (MIN_PER_T[t] - per_t[t])

            if numbering[0] + numbering[Tn] - numbering[last_event] > MAX_BETWEEN:
                values['penalty_max_between'] = values['penalty_max_between'] + \
                    COST_MAX_BETWEEN * \
                    (numbering[0] + numbering[Tn] -
                     numbering[last_event] - MAX_BETWEEN)
    return values
