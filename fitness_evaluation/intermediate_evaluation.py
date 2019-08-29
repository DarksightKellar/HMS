from fitness_evaluation.costs import *
from fitness_evaluation.numbering import Numbering


def intermediate_evaluation(Numberings, values, schedule, event_n):
    '''
    Returns `'no event'` if event_n doesn't exist, i.e there's no nth event
    '''
    numbering_i = 0
    for numbering in Numberings:
        numbering: Numbering

        last_nr = values['last_nr'][numbering_i]

        event_numbering = numbering.get_nth_event_numbering(event_n, schedule) # event_numberings[numbering_i]

        if event_numbering is False:
            return 'no event'

        if event_numbering != None:
            values['total'][numbering_i] += 1

            if last_nr is not None and event_numbering == last_nr + 1:
                values['consecutive'][numbering_i] += 1

            elif last_nr is not None and event_numbering > last_nr + 1:
                if values['consecutive'][numbering_i] < numbering.min_consecutive: # MIN_CONSECUTIVE[numbering_i]:
                    values['penalty_min_consecutive'][numbering_i] += numbering.cost_min_consecutive  * \
                        (numbering.min_consecutive - values['consecutive'][numbering_i])

                if values['consecutive'][numbering_i] > numbering.max_consecutive:
                    values['penalty_max_consecutive'][numbering_i]  += numbering.cost_max_consecutive * \
                        (values['consecutive'][numbering_i] - numbering.max_consecutive)

                if event_numbering - last_nr - 1 < numbering.min_between:
                    values['penalty_min_between'][numbering_i] += numbering.cost_min_between * \
                        (numbering.min_between - (event_numbering - last_nr - 1))

                if event_numbering - last_nr - 1 > numbering.max_between:
                    values['penalty_max_between'][numbering_i] += numbering.cost_max_between * \
                        ((event_numbering - last_nr - 1) - numbering.max_between)
                
                values['consecutive'][numbering_i] = 1

            values['per_t'][numbering_i][event_numbering] += 1
            values['last_nr'][numbering_i] = event_numbering
        
        numbering_i += 1
