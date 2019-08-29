from instance import Instance
from math import ceil
from helper_classes.nurse import *
from helper_classes.skills import *
from helper_classes.parse_xml import parseXML

def create_instance(self):
    data = parseXML('helper_classes/test_data/sprint_early/sprint01.xml')
    '''
    data = {
        'number_of_days': number_of_days,
        'skills': skills,
        'shift_types': shift_types,
        'shift_skills': shift_skills,
        'shift_ids': shift_ids,
        'patterns': patterns,
        'contracts': contracts,
        'nurses': nurses,
        'cover_requirements': cover_requirements,
        'day_off_requests': day_off_requests,
        'shift_off_requests': shift_off_requests
    }
    '''


    N_DAYS = data['number_of_days']
    N_SHIFTS = len(data['shift_types'])
    N_ALLOCATIONS = N_DAYS * N_SHIFTS

    # create 10 nurses, including 2 NOs
    nurses = data['nurses']
    contracts = data['contracts']

    skills = data['skills']
    shift_types = data['shift_types']
    scheduling_period = N_DAYS

    n_weeks = N_DAYS / 7
    cover_request_matrix = data['cover_requirements'] * n_weeks

    patterns = data['patterns']

    # In the matrices below,
    #   0    - request off
    #   1    - request on
    #   None - no request made for that shift
    day_request_matrix = [None for _ in range(N_DAYS) for _ in range(len(nurses))]
    # day_on_matrix = [None for _ in range(N_DAYS) for _ in range(len(nurses))]
    shift_request_matrix = [None for _ in range(N_ALLOCATIONS) for _ in range(len(nurses))]
    # shift_on_matrix = [None for _ in range(N_ALLOCATIONS) for _ in range(len(nurses))]

    for day_off_request in data['day_off_requests']:
        # [day_number, nurse_id, weight]
        day_index = day_off_request[0] - 1
        nurse_index = day_off_request[1]
        weight = day_off_request[2]

        # Update matrix to add this request
        day_request_matrix[nurse_index][day_index] = 0

    for shift_off_request in data['shift_off_requests']:
        # [day_number, shift_id, nurse_id, weight]
        day_number = shift_off_request[0]
        shift_id = shift_off_request[1]
        nurse_index = shift_off_request[2]
        weight = shift_off_request[3]

        
        # Get to 1st shift of day `day_number` 
        shift_index = 0
        for day_n in range(day_number-1):
            for i in range(N_SHIFTS):
                shift_index += 1

        # Figure out which shift within the day the request is made for
        offset = data['shift_ids'].index(shift_id)
        shift_index += offset

        # Update matrix to add this request
        shift_request_matrix[nurse_index][shift_index] = 0

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
        day_request_matrix, [], shift_request_matrix, [])