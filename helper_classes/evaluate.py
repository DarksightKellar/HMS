from helper_classes.shift import Shift
from helper_classes.nurse import Nurse
from helper_classes.skills import *
from helper_classes.constants import N_DAYS, N_SHIFTS
from helper_classes.contract import Contract
from helper_classes.write_xml import writeXML
from helper_classes.test_data.filenames import *

from fitness_evaluation.eval import evaluate
from fitness_evaluation.numbering import Numbering

import os

def evaluate_harmony(harmony, instance):
    writeXML(SOLUTION_XML, 'Test', instance, harmony)

    cmd = str.format('java -jar data/evaluate.jar -p {} -s {}', INSTANCE_XML, SOLUTION_XML)
    output = os.popen(cmd).read()
    
    results = output.split('\n')
    hard_constraint_cost = float(results[0].split(':')[1])
    soft_constraint_cost = float(results[1].split(':')[1])

    return [hard_constraint_cost, soft_constraint_cost]


def get_cost(vals):
    cost = 0
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

def update_details(res, details):
    # TODO: Update constraint violation details
    pass

def evaluate_solution(solution, shifts, prev_solution=[], contracts=[], reject_empty_shift=True) -> int:
    '''
    Evaluate a solution, returns `[cost, details]` of the solution,
    with `details` containing details of any constraint violations.

    Returns `None` if solution is infeasible
    '''

    total_cost = 0
    details = {}

    i = 0
    if len(prev_solution) == 0:
        prev_solution = [[0 for _ in range(len(shifts))] for _ in range(len(solution))]

    if len(contracts) == 0:
        contracts = [Contract() for _ in range(len(solution))]

    for schedule in solution:
        prev_schedule = prev_solution[i]

        contract: Contract = contracts[i]
        __numberings__ = contract.numberings
        
        numberings = [n.get_numberings() for n in __numberings__]
        prev_numberings = [n.get_previous() for n in __numberings__]
        m_list = [n.get_M() for n in __numberings__]

        res = evaluate(schedule, prev_schedule, __numberings__, contract)
        update_details(res, details)

        # Infeasible solution if a nurse has multiple assignments for any day
        for per_t in res['per_t'][0]:
            if per_t > 1:
                return [None, details]
        
        # Infeasible solution if a nurse has a morning after night shift
        for per_t in res['per_t'][1]:
            if per_t > 1:
                return [None, details]

        total_cost += get_cost(res)
        i += 1

    # check shift requirements
    a_shift_is_empty = False
    for shift in shifts:
        shift: Shift

        # Infeasible solution if a shift has no nurses assigned to it
        if len(shift.assigned_nurses) == 0:
            a_shift_is_empty = True
            total_cost += 10

        for requirement in shift.skills_required:
            requirement: SkillRequired

            n_assigned_nurses_with_skill = 0
            for assignee in shift.assigned_nurses:
                assignee: Nurse

                if requirement.skill in assignee.skills:
                    n_assigned_nurses_with_skill += 1

            deficit = requirement.required - n_assigned_nurses_with_skill

            # Under-staffing
            if deficit > 0:
                total_cost += requirement.cost * deficit*3

            # Over-staffing
            if deficit < 0:
                penalty = -1 * deficit
                total_cost += (requirement.cost * penalty * 3) ** penalty

    if reject_empty_shift and a_shift_is_empty:
        return None

    return total_cost
