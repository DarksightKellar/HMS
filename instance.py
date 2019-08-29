from helper_classes.constants import *
from math import ceil
from helper_classes.nurse import *
from helper_classes.skills import *


class Instance():
    def __init__(self, nurses, shifts, contracts, skills, shift_types, scheduling_period, cover_request_matrix,
                day_off_matrix, day_on_matrix, shift_off_matrix, shift_on_matrix):
        self.nurses = nurses
        self.shifts = shifts
        self.contracts = contracts
        self.skills = skills
        self.shift_types = shift_types  # set of possible shift types
        self.scheduling_period = scheduling_period  # ie, number of days per period
        self.cover_request_matrix = cover_request_matrix  # is this the demand?
        self.day_off_matrix = day_off_matrix
        self.day_on_matrix = day_on_matrix
        self.shift_off_matrix = shift_off_matrix
        self.shift_on_matrix = shift_on_matrix

    @classmethod
    def create_test_instance(self):
        # create 10 nurses, including 2 NOs
        nurses = []
        for i in range(8):
            nurses.append(Nurse(id, last_name=str.format('Mansa{}',i), other_names=str.format('{}Yaa',i), skills=[NurseSkill]))

        for i in range(2):
            nurses.append(Nurse(id, last_name=str.format('Baako{}',i), other_names=str.format('{}Ama',i), skills=[NurseSkill, NursingOfficerSkill]))

        contracts = []

        skills = [NurseSkill, NursingOfficerSkill]
        shift_types = ['morning', 'afternoon', 'night']
        scheduling_period = N_DAYS

        cover_request_matrix = []
        day_off_matrix = []
        day_on_matrix = []
        shift_off_matrix = []
        shift_on_matrix = []

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

        return Instance(nurses, shifts, contracts, skills, 
            shift_types, scheduling_period, cover_request_matrix, 
            day_off_matrix, day_on_matrix, shift_off_matrix, shift_on_matrix)

