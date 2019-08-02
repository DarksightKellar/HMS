from typing import List
# burke et al (2008)

# combining a variable neighbourhood search with
# heuristically unassigning shifts and repairing
# schedules, using heuristic ordering

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

    final_schedule = [[0 for _ in range(n_shifts)] for _ in range(n_nurses)]

    # Apply weight evaluation function to each shift's weight
    # to determine assignment difficulty
    for shift in shifts:
        shift.evaluate()

    # Sort shifts (decreasing order of assignment difficulty)
    sorted_shifts = sorted(shifts, key=lambda shift: shift.assignment_difficulty, reverse=True)

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


if __name__ == '__main__':
    from helper_classes.constants import *

    # create nurses
    nurses = []
    for i in range(10):
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
            SkillRequired(NurseSkill, nurses_required)
        ]

        if is_night_shift:
            # require one qualified nursing officer on night shifts
            skills_required.append(SkillRequired(NursingOfficerSkill, 1))
            weight += NIGHT_SHIFT_WEIGHT

            n_valid_nurses = count_skills(nurses, skills_required)
            n_nurses = len(nurses)

            # add weight to this new requirement
            extra_weight = (n_nurses/n_valid_nurses) * SKILL_WEIGHT
            weight += extra_weight
        
        if is_weekend:
            weight += WEEKEND_SHIFT_WEIGHT

        # add weight to shifts the later they occur
        weight += SHIFT_DATE_WEIGHT * (N_ALLOCATIONS - i)
        
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
    print(x)