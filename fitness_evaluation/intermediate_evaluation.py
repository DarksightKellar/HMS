from constraints import *
from costs import *


def intermediate_evaluation(Numberings, event, values):
    # n_numberings = len(Numberings)

    numbering_i = 0
    for numbering in Numberings:
        last_nr = values['N_last_nr'][numbering_i]

        event_numbering = numbering[event]

        if event_numbering != None:
            values['total'] = values['total'] + 1

            if event_numbering == last_nr + 1:
                values['consecutive'] = values['consecutive'] + 1

            elif event_numbering > last_nr + 1:
                if values['consecutive'] < MIN_CONSECUTIVE:
                    values['penalty_min_consecutive'] = values['penalty_min_consecutive'] + \
                        COST_MIN_CONSECUTIVE * \
                        (MIN_CONSECUTIVE - values['consecutive'])

                if values['consecutive'] > MAX_CONSECUTIVE:
                    values['penalty_max_consecutive'] = values['penalty_max_consecutive'] + \
                        COST_MAX_CONSECUTIVE * \
                        (MAX_CONSECUTIVE - values['consecutive'])

                if event_numbering - last_nr - 1 < MIN_BETWEEN:
                    values['penalty_min_between'] = values['penalty_min_between'] + \
                        COST_MIN_BETWEEN * \
                        (MIN_BETWEEN - (event_numbering - last_nr - 1))

                if event_numbering - last_nr - 1 > MAX_BETWEEN:
                    values['penalty_max_between'] = values['penalty_max_between'] + \
                        COST_MAX_BETWEEN * \
                        ((event_numbering - last_nr - 1) - MAX_BETWEEN)

            values['per_t'][numbering_i][event_numbering] = values['per_t'][numbering_i][event_numbering] + 1
            values['N_last_nr'][numbering_i] = event_numbering
        
        numbering_i = numbering_i + 1
