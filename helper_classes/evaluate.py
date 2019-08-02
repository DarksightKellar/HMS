from helper_classes.shift import Shift
from fitness_evaluation.eval import evaluate 
from fitness_evaluation.constraints import N0, N1, N2, pN0, pN1, pN2, M_LIST


def evaluate_harmony(harmony):
    return 0


def get_cost(vals):
    cost = 0
    for c in vals['penalty_min_consecutive']:
        cost += c

    for c in vals['penalty_min_consecutive']:
        cost += c

    for c in vals['penalty_max_consecutive']:
        cost += c

    for c in vals['penalty_min_between']:
        cost += c

    for c in vals['penalty_max_between']:
        cost += c

    for c in vals['penalty_max_total']:
        cost += c

    for c in vals['penalty_min_total']:
        cost += c

    for n in vals['penalty_max_per_t']:
        for c in n:
            cost += c

    return cost


def evaluate_solution(solution, shifts, constraints=[]) -> int:
    '''
    Evaluate a solution, returns `cost` of the solution

    Returns `-1` if solution is infeasible
    '''

    for schedule in solution:
        prev_schedule = [0 for _ in range(len(shifts))]
        numberings = [N0, N1, N2]
        prev_numberings = [pN0, pN1, pN2]

        res = evaluate(schedule, prev_schedule, numberings, prev_numberings)
        cost = get_cost(res)


    return cost
