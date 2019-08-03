N_DAYS = 7
N_SHIFTS = 3
N_ALLOCATIONS = N_DAYS * N_SHIFTS
NIGHT_SHIFT_WEIGHT = 100
WEEKEND_SHIFT_WEIGHT = 50
SKILL_WEIGHT = 70
SHIFT_DATE_WEIGHT = 20

# Skills
from helper_classes.skills import Skill
NurseSkill = Skill('Nurse')
NursingOfficerSkill = Skill("Nursing Officer")

COST_NURSE_REQ = 2
COST_NURSING_OFFICER_REQ = 5