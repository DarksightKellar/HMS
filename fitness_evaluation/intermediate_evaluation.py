from constraints import *
from costs import *


def intermediate_evaluation(Numberings, event, values, last_nr):
    # n_numberings = len(Numberings)

    for numbering in Numberings:
        event_numbering = numbering[event]

        if event_numbering != None:
            values['total'] = values['total'] + 1

            if event_numbering == last_nr + 1:
                values['consecutive'] = values['consecutive'] + 1

            elif event_numbering > last_nr + 1:
                if values['consecutive'] < MAX_CONSECUTIVE:
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

            values['per_t'][event_numbering] = values['per_t'][event_numbering] + 1
            last_nr = event_numbering
