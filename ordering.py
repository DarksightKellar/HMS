from typing import List

import random

from helper_classes.evaluate import evaluate_solution
from helper_classes.nurse import Nurse
from helper_classes.shift import Shift
from helper_classes.skills import Skill, SkillRequired


def ordering(shifts: List[Shift], nurses: List[Nurse]) -> List:
    '''
    `shifts` A list of Shift objects

    `nurses` A list of Nurse objects
    '''

    # Duplicate shifts and nurses so modifications don't affect them
    _nurses = []
    _shifts = []
    
    for n in nurses:
        _nurses.append(n.duplicate())  

    # each nurse in nurses is a list of `n_shifts` 0-1 allocations for each shift in shifts
    n_shifts = len(shifts)
    n_nurses = len(nurses)

    assert(n_shifts == nurses[0].n_allocations)

    final_schedule = []
    contracts = [n.contract for n in nurses]

    # Apply weight evaluation function to each shift's weight
    # to determine assignment difficulty
    for shift in shifts:
        _shift = shift.duplicate()
        _shift.evaluate()
        _shifts.append(_shift)

    # Sort shifts (decreasing order of assignment difficulty)
    sorted_shifts = sorted(_shifts, key=lambda shift: shift.assignment_difficulty, reverse=True)

    # Randomise nurses
    random_nurses = random.sample(_nurses, len(_nurses))

    # for each sorted shift, assign this to the nurse that incurs lowest cost
    best_cost = None
    for shift in sorted_shifts:
        shift: Shift

        # None implies this shift hasn't been previously assigned yet
        shift_best_cost = None

        # track the nurse that incurs the best cost for this shift, even 
        # if this cost might be worse than best_cost
        tentative_best_nurse = None

        # for this shift, the previously assigned nurse with best cost.
        # None implies algorithm hasn't begun
        best_nurse = None

        # find first nurse unassigned to slot, then try assigning them to see resulting cost
        cost = None
        for nurse in random_nurses:
            nurse: Nurse

            # if this nurse has already been assigned this shift, skip to next nurse
            if nurse.allocations[shift.index] == 1:
                continue

            # assign this nurse to this shift
            nurse.assign(shift)

            solution = [n.allocations for n in _nurses]
            cost = evaluate_solution(solution, _shifts, contracts=contracts)
            if shift_best_cost is None:
                shift_best_cost = cost
            
            if best_cost is None:
                best_cost = cost

            # print(cost)

            # TODO: Possible research point:
            # Is it better to try to improve the naively feasible solution here,
            # or allow HMS to do all the optimisation work?

            if cost is None or cost > best_cost:
                # this cost is worse or contributes nothing, undo this assignment
                # print(str.format('worse. best cost is {}', best_cost))
                nurse.unassign(shift)
                if best_nurse is not None:
                    best_nurse.assign(shift)
                
                if cost is not None:
                    # Then we're ignoring this assignment even though solution is feasible
                    if not cost > shift_best_cost:
                        shift_best_cost = cost
                        tentative_best_nurse = nurse

            elif cost < best_cost:
                # this cost is better, save it
                # print(str.format('better than best cost of {}', best_cost))
                best_cost = cost
                shift_best_cost = cost

                # note that we leave the previous nurse assignment with former best cost unassigned

                # save this nurse as best assigned nurse for future reference
                best_nurse = nurse
                tentative_best_nurse = nurse

        if best_nurse is None:
            if tentative_best_nurse is None:
                0 # print('FEASIBLE SOLUTION NOT FOUND')
            else:
                    tentative_best_nurse.assign(shift)

        # so that subsequent shift logic will not re-append to _nurses
        nurses_duplicated = True 

    for n in _nurses:
        final_schedule.append(n.allocations.copy())

    return [final_schedule, best_cost]