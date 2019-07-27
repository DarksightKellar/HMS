from constraints import *
from costs import *


def intermediate_evaluation(Numberings, event_numberings, values):
    numbering_i = 0
    for numbering in Numberings:
        last_nr = values['last_nr'][numbering_i]

        event_numbering = event_numberings[numbering_i]

        if event_numbering != None:
            values['total'][numbering_i] += 1

            if last_nr is not None and event_numbering == last_nr + 1:
                values['consecutive'][numbering_i] += 1

            elif last_nr is not None and event_numbering > last_nr + 1:
                if values['consecutive'][numbering_i] < MIN_CONSECUTIVE:
                    values['penalty_min_consecutive'][numbering_i] += COST_MIN_CONSECUTIVE * \
                        (MIN_CONSECUTIVE - values['consecutive'][numbering_i])

                if values['consecutive'][numbering_i] > MAX_CONSECUTIVE:
                    values['penalty_max_consecutive'][numbering_i]  += COST_MAX_CONSECUTIVE * \
                        (MAX_CONSECUTIVE - values['consecutive'][numbering_i])

                if event_numbering - last_nr - 1 < MIN_BETWEEN:
                    values['penalty_min_between'][numbering_i] += COST_MIN_BETWEEN * \
                        (MIN_BETWEEN - (event_numbering - last_nr - 1))

                if event_numbering - last_nr - 1 > MAX_BETWEEN:
                    values['penalty_max_between'][numbering_i] += COST_MAX_BETWEEN * \
                        ((event_numbering - last_nr - 1) - MAX_BETWEEN)

            values['per_t'][numbering_i][event_numbering] += 1
            values['last_nr'][numbering_i] = event_numbering
        
        numbering_i += 1
