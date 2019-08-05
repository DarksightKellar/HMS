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

    # each nurse in nurses is a list of `n_shifts` 0-1 allocations for each shift in shifts
    n_shifts = len(shifts)
    n_nurses = len(nurses)

    assert(n_shifts == nurses[0].n_allocations)

    final_schedule = []

    # Apply weight evaluation function to each shift's weight
    # to determine assignment difficulty
    for shift in shifts:
        shift.evaluate()

    # Sort shifts (decreasing order of assignment difficulty)
    sorted_shifts = sorted(shifts, key=lambda shift: shift.assignment_difficulty, reverse=True)

    # Randomise nurses
    random_nurses = random.sample(nurses, len(nurses))

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


            cost = evaluate_solution([n.allocations for n in nurses], shifts)
            if shift_best_cost is None:
                shift_best_cost = cost
            
            if best_cost is None:
                best_cost = cost

            print(cost)

            # Possible research point:
            # Is it better to try to improve the naively feasible solution here,
            # or allow HMS to do all the optimisation work?

            if cost is None or cost > best_cost:
                # this cost is worse or contributes nothing, undo this assignment
                print(str.format('worse. best cost is {}', best_cost))
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
                print(str.format('better than best cost of {}', best_cost))
                best_cost = cost
                shift_best_cost = cost

                # note that we leave the previous nurse assignment with former best cost unassigned

                # save this nurse as best assigned nurse for future reference
                best_nurse = nurse
                tentative_best_nurse = nurse

        if best_nurse is None:
            if tentative_best_nurse is None:
                print('FEASIBLE SOLUTION NOT FOUND')
            else:
                    tentative_best_nurse.assign(shift)

    for n in nurses:
        final_schedule.append(n.allocations)

    return final_schedule


def count_skills(nurses, skills_required: List[SkillRequired]):
    count = 0
    for nurse in nurses:
        invalid = False
        for req_skill in skills_required:
            if req_skill.skill in nurse.skills:
                continue
            else:
                invalid = True
                break
        
        if not invalid:
            count += 1

    return count


def test_fit_eval():
    import pprint as pp
    from fitness_evaluation.constraints import \
        pN0, pN1, pN2, \
        N0, N1, N2, M_LIST
    from fitness_evaluation.eval import evaluate
    
    prev_schedule = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0, 1,0,0, 1,0,0]

    schedule = [1,0,0, 1,0,0, 1,0,0, 0,1,0, 0,0,1, 0,0,0, 0,0,0]
    schedule2 = [1,0,0, 1,0,0, 1,0,0, 0,0,0, 0,0,0, 0,0,0, 1,0,0]
    schedule3 = [0,0,0, 0,0,0, 0,0,1, 0,0,0, 0,0,0, 0,0,0, 0,0,1]
    

    numberings = [N0, N1, N2]
    prev_numberings = [pN0, pN1, pN2]
    print(evaluate(schedule3, prev_schedule, numberings, prev_numberings))


def nicelyprintresults(res):
    print('')
    pp.pprint(res)
    print('')


if __name__ == '__main__':
    # test_fit_eval()

    from helper_classes.constants import *
    from math import ceil
    
    import pprint as pp

    

    # create 12 nurses, including 2 NOs
    nurses = []
    for i in range(8):
        nurses.append(Nurse(id, last_name=str.format('Mansa{}',i), other_names=str.format('{}Yaa',i), skills=[NurseSkill], max_assignments=5))

    for i in range(2):
        nurses.append(Nurse(id, last_name=str.format('Baako{}',i), other_names=str.format('{}Ama',i), skills=[NurseSkill, NursingOfficerSkill], max_assignments=5))
        
    
    # create weighted shifts
    shifts = []

    for i in range(N_ALLOCATIONS):
        is_morning_shift = i % 3 == 0
        is_afternoon_shift = i % 3 == 1
        is_night_shift = i % 3 == 2

        is_weekend = i % 21 in [15,16,17,18,19,20]

        shift = 'morning' if is_morning_shift else 'afternoon' if is_afternoon_shift else 'night'
        nurses_required = 3 if is_morning_shift else 5 if is_afternoon_shift else 2
        weight = 0

        # different nurse requirements for weekend shifts
        if is_weekend:
            nurses_required = 1 if is_night_shift else 2

        # skills_required specify the minimum number required for the shift
        # Aside that, all base nurses count toward the total staff requirement
        skills_required = [
            SkillRequired(NurseSkill, nurses_required, COST_NURSE_REQ)
        ]

        if is_night_shift:
            # require one qualified nursing officer on night shifts
            skills_required.append(SkillRequired(NursingOfficerSkill, 1, COST_NURSING_OFFICER_REQ))
            weight += NIGHT_SHIFT_WEIGHT

            n_valid_nurses = count_skills(nurses, skills_required)
            n_nurses = len(nurses)

            # add weight to this new requirement
            extra_weight = (n_nurses/n_valid_nurses) * SKILL_WEIGHT
            weight += extra_weight
        
        if is_weekend:
            weight += WEEKEND_SHIFT_WEIGHT

        # add more weight to shifts the later they occur
        days_to_end_of_period = ceil((N_ALLOCATIONS - i) / N_SHIFTS)
        weight += SHIFT_DATE_WEIGHT *  days_to_end_of_period

        multiplier = 1

        shifts.append(Shift(
            index=i,
            shift_type=shift,
            skills_required=skills_required,
            n_nurses_required=nurses_required, 
            weight=weight,
            evaluation_multiplier=multiplier
        ))


    x = ordering(shifts, nurses)
    cost = evaluate_solution(x, shifts)
    nicelyprintresults(x)
    print(cost)