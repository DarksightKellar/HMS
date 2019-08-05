from helper_classes.shift import Shift
from helper_classes.nurse import Nurse
from helper_classes.skills import *
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

    Returns `None` if solution is infeasible
    '''

    total_cost = 0
    for schedule in solution:
        prev_schedule = [0 for _ in range(len(shifts))]
        numberings = [N0, N1, N2]
        prev_numberings = [pN0, pN1, pN2]

        res = evaluate(schedule, prev_schedule, numberings, prev_numberings)

        for per_t in res['per_t'][0]:
            if per_t > 1:
                return None

        total_cost += get_cost(res)

    for shift in shifts:
        shift: Shift

        # check shift requirements
        for requirement in shift.skills_required:
            requirement: SkillRequired

            n_assigned_nurses_with_skill = 0
            for assignee in shift.assigned_nurses:
                assignee: Nurse

                if requirement.skill in assignee.skills:
                    n_assigned_nurses_with_skill += 1

            deficit = requirement.required - n_assigned_nurses_with_skill

            # if shift.shift_type == 'night' and requirement.required == 1 and deficit
            
            if deficit > 0:
                total_cost += requirement.cost * deficit*deficit

            if deficit < -1 * (requirement.required / 2):
                total_cost += -1 * deficit/2 * requirement.cost * 10

    return total_cost
