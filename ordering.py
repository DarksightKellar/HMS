# burke et al (2008)

# combining a variable neighbourhood search with
# heuristically unassigning shifts and repairing
# schedules, using heuristic ordering


def ordering(shifts, nurses):
    n_shifts = len(shifts)
    n_nurses = len(nurses)

    # Apply weight evaluation function to each shift's weight
    # to determine final rank
    for shift in shifts:
        shift.rank = shift.eval_func(shift.weight)

    # Sort shifts in order of ranks
    sorted_shifts = sorted(shifts, key=lambda shift: shift.rank, reverse=True)

    # for each sorted shift, assign this to the free nurse with lowest cost
    for shift in sorted_shifts:
        pass

    initial_schedule = []
    return initial_schedule
