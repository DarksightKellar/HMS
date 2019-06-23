# burke et al (2008)

# combining a variable neighbourhood search with
# heuristically unassigning shifts and repairing
# schedules, using heuristic ordering

from helper_classes.evaluate import evaluate_solution
from helper_classes.shift import Shift
from helper_classes.nurse import Nurse


def ordering(shifts, nurses):
    '''
    `shifts` An array of Shift objects

    `nurses` An array of Nurse objects
    '''
    # each nurse in nurses is a list of n_shifts 0-1 allocations, for each shift in shifts

    n_shifts = len(shifts)
    n_nurses = len(nurses)

    assert(n_shifts == nurses[0].n_allocations)

    final_schedule = [[0 for _ in range(n_shifts)] for _ in range(n_nurses)]

    # Apply weight evaluation function to each shift's weight
    # to determine assignment difficulty
    for i, shift in shifts:
        shift.evaluate()

    # Sort shifts (decreasing order of assignment difficulty)
    sorted_shifts = sorted(
        shifts, key=lambda shift: shift.assignment_difficulty, reverse=True)

    # for each sorted shift, assign this to the nurse that incurs lowest cost
    for shift in sorted_shifts:
        shift: Shift

        # None implies this shift hasn't been previously assigned yet
        best_cost = None

        # for this shift, the previously assigned nurse with best cost.
        # None implies algorithm hasn't begun
        best_nurse = None

        # find first nurse unassigned to slot, then try assigning them to see resulting cost
        for nurse in nurses:
            nurse: Nurse

            # if this nurse has already been assigned this shift, skip to next nurse
            if nurse.allocations[shift.index] == 1:
                continue

            # assign this nurse to this shift
            nurse.assign(shift)

            # unschedule this shift's assigned nurse, if it has a previous assignee
            if best_nurse is not None:
                best_nurse.unassign(shift)

            cost = evaluate_solution([n.allocations for n in nurses], shifts)

            # Possible research point:
            # Is it better to try to improve the naively feasible solution here,
            # or allow HMS to do all the optimisation work?

            if cost is None or (best_cost is not None and cost > best_cost):
                # this cost is worse, undo this assignment
                nurse.unassign(shift)
                if best_nurse is not None:
                    best_nurse.assign(shift)
            else:
                # this cost is better, save it
                best_cost = cost

                # note that we leave the previous nurse assignment with former best cost unassigned

                # save this nurse as best assigned nurse for future reference
                best_nurse = nurse

    return final_schedule
