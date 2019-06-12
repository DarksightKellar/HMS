# burke et al (2008)

# combining a variable neighbourhood search with
# heuristically unassigning shifts and repairing
# schedules, using heuristic ordering

from evaluate import evaluate_solution


def ordering(shifts, nurses):
    '''
    shift in shifts should have at least
    `eval_func()`
    `weight`
    '''
    # each nurse in nurses is a list of n_shifts 0-1 allocations, for each shift in shifts

    n_shifts = len(shifts)
    n_nurses = len(nurses)

    final_schedule = [[0 for _ in range(n_shifts)] for _ in range(n_nurses)]

    # Apply weight evaluation function to each shift's weight
    # to determine final rank
    for i, shift in shifts:
        shift.rank = shift.eval_func(shift.weight)

        # each shift should have an integer id parameter so that sorting doesn't destroy its
        # original position
        if not shift.id:
            shift.id = i

    # Sort shifts in order of ranks (decreasing order of assignment difficulty)
    sorted_shifts = sorted(shifts, key=lambda shift: shift.rank, reverse=True)

    # for each sorted shift, assign this to the nurse that incurs lowest cost
    for shift_idx, shift in sorted_shifts:
        # None implies this shift hasn't been previously assigned yet
        best_cost = None

        # for this shift, the index of previously assigned nurse with best cost.
        # None implies algorithm hasn't begun
        best_nurse_idx = None

        # find a nurse with unassigned slot, then try assigning them
        for nurse_idx, _ in nurses:
            nurse_schedule = final_schedule[nurse_idx]

            # if last assignment slot is assigned, skip this nurse
            if nurse_schedule[n_shifts-1] == 1:
                continue

            # assign this nurse to this shift
            nurse_schedule[shift_idx] = 1

            # unschedule this shift's assigned nurse, if it has a previous assignee
            if best_nurse_idx is not None:
                final_schedule[best_nurse_idx][shift_idx] = 0

            cost = evaluate_solution(final_schedule)

            if best_cost is not None and cost > best_cost:
                # this cost is worse, undo this assignment
                nurse_schedule[shift_idx] = 0
                if best_nurse_idx is not None:
                    final_schedule[best_nurse_idx][shift_idx] = 1
            else:
                # this cost is better, save it
                best_cost = cost

                # note that we leave the previous nurse assignment with former best cost unassigned

                # save this nurse index as best assigned nurse index for future reference
                best_nurse_idx = nurse_idx

    return final_schedule
