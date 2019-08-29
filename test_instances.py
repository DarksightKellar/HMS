from instance import Instance
from math import ceil
from helper_classes.nurse import *
from helper_classes.skills import *
from helper_classes.parse_xml import parseXML

def create_instance():
    data = parseXML('helper_classes/test_data/sprint_early/sprint01.xml')
    '''
    data = {
        'number_of_days': number_of_days,
        'skills': skills,
        'shift_types': shift_types,
        'shift_skills': shift_skills,
        'shift_ids': shift_ids,
        'shift_weights': shift_weights,
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
    shift_skills = data['shift_skills']
    shift_weights = data['shift_weights']

    assert(len(shift_types) == len(shift_skills))
    assert(len(shift_skills) == len(shift_weights))

    scheduling_period = N_DAYS

    n_weeks = int(N_DAYS / 7)
    cover_request_matrix = data['cover_requirements'] * n_weeks

    patterns = data['patterns']

    # In the matrices below,
    #   0    - request off
    #   1    - request on
    #   None - no request made for that shift
    day_request_matrix = [[None for _ in range(N_DAYS)] for _ in range(len(nurses))]
    shift_request_matrix = [[None for _ in range(N_ALLOCATIONS)] for _ in range(len(nurses))]

    for day_off_request in data['day_off_requests']:
        # [day_number, nurse_id, weight]
        day_index = day_off_request[0] - 1
        nurse_index = int(day_off_request[1])
        weight = day_off_request[2]

        # Update matrix to add this request
        day_request_matrix[nurse_index][day_index] = 0

    for shift_off_request in data['shift_off_requests']:
        # [day_number, shift_id, nurse_id, weight]
        day_number = shift_off_request[0]
        shift_id = shift_off_request[1]
        nurse_index = int(shift_off_request[2])
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

    # generate indices of shifts belonging to weekend 
    weekend_indices = []
    n_weeks = int(N_ALLOCATIONS / 7 / N_SHIFTS)
    for week_n in range(n_weeks):
        start_idx = N_SHIFTS * ((week_n+1) * 7) - 2*N_SHIFTS
        end_idx = start_idx + 2*N_SHIFTS - 1

        for idx in range(start_idx, end_idx+1):
            weekend_indices.append(idx)

    # create weighted shifts
    shifts = []
    for i in range(N_ALLOCATIONS):
        shift_type_index = i % N_SHIFTS

        is_weekend = i in weekend_indices

        nurses_required = cover_request_matrix[i]
        weight = shift_weights[shift_type_index]

        _skills = shift_skills[shift_type_index]
        skills_required = [SkillRequired(skill, nurses_required, 1) for skill in _skills]
        
        if is_weekend:
            weight += WEEKEND_SHIFT_WEIGHT

        # add more weight to shifts the later they occur
        days_to_end_of_period = ceil((N_ALLOCATIONS - i) / N_SHIFTS)
        weight += SHIFT_DATE_WEIGHT *  days_to_end_of_period

        multiplier = 1

        shifts.append(Shift(
            index=i,
            shift_type=shift_types[shift_type_index],
            skills_required=skills_required,
            n_nurses_required=nurses_required, 
            weight=weight,
            evaluation_multiplier=multiplier
        ))

    return Instance(nurses, shifts, contracts, skills, 
        shift_types, scheduling_period, cover_request_matrix, 
        day_request_matrix, shift_request_matrix)