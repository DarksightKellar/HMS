from math import ceil
from helper_classes.nurse import *
from helper_classes.skills import *
from helper_classes.contract import *

import xml.etree.ElementTree as ET 

def parseXML(xmlfile): 

    # create element tree object 
    tree = ET.parse(xmlfile) 

    # get root SchedulingPeriod element 
    root = tree.getroot()

    startDay = int(str(root.find('StartDate').text).split('-')[2])
    endDay = int(str(root.find('EndDate').text).split('-')[2])

    assert startDay == 1

    number_of_days = endDay - startDay + 1 # int(root.attrib['nDays'])
    skills = [] 
    shift_types = []
    shift_skills = []
    shift_ids = []
    shift_weights = []
    patterns = []
    contracts = []
    nurses = []
    cover_requirements = []
    day_off_requests = []
    shift_off_requests = []


    # retrieve skills
    for skill in root.findall('./Skills/Skill'):
        skills.append(Skill(str(skill.text)))

    # retrieve shift types, and associated required skills
    for shift in root.findall('./ShiftTypes/Shift'):
        # for shift in st.findall('Shift'):
        shift_types.append(str(shift.find('Description').text))
        shift_skills.append([Skill(str(sk.text)) for sk in shift.findall('Skills/Skill')])
        shift_ids.append(str(shift.attrib['ID']))
        shift_weights.append(int(shift.attrib['weight']))

    # retrieve patterns
    for pattern in root.findall('./Patterns/Pattern'):
        pass

    # retrieve contracts
    for contract in root.findall('./Contracts/Contract'):
        min_total = int(contract.find('MinNumAssignments').text)
        max_total = int(contract.find('MaxNumAssignments').text)

        min_consecutive = int(contract.find('MinConsecutiveWorkingDays').text)
        max_consecutive = int(contract.find('MaxConsecutiveWorkingDays').text)
        
        min_between = int(contract.find('MinConsecutiveFreeDays').text)
        max_between = int(contract.find('MaxConsecutiveFreeDays').text)

        contracts.append(Contract(
            limit_total=[min_total, max_total],
            limit_consecutive=[min_consecutive, max_consecutive],
            limit_between=[min_between, max_between],
            n_days=number_of_days,
            n_shifts=len(shift_types)
        ))

    # retrieve nurses
    for n in root.findall('./Employees/Employee'):
        names = str(n.find('Name').text).split(' ')
        nurse_skills = [ Skill(str(sk.text)) for sk in n.find('Skills') ]
        contract_id = int(n.find('ContractID').text)
        nurse_id = str(n.attrib['ID'])

        nurse = Nurse(
            id, names[len(names)-1], names[0:len(names)-1], 
            nurse_skills, contracts[contract_id],
            nurse_id=nurse_id, n_allocations=number_of_days*len(shift_types)
        )

        nurses.append(nurse)

    # retrieve cover requirements
    for dayofweekcover in root.findall('./CoverRequirements/DayOfWeekCover'):
        day_of_week_requirements = [int(cover.find('Preferred').text) for cover in dayofweekcover.findall('Cover')]
        
        for r in day_of_week_requirements:
            cover_requirements.append(r)

    # retrieve day off requests
    for day_off in root.findall('./DayOffRequests/DayOff'):
        _date = str(day_off.find('Date').text)
        day_number = int(_date.split('-')[2])
        nurse_id = str(day_off.find('EmployeeID').text)
        weight = int(day_off.attrib['weight'])

        day_off_requests.append([day_number, nurse_id, weight])

    # retrieve shift off requests
    for shift_off in root.findall('./ShiftOffRequests/ShiftOff'):
        _date = str(shift_off.find('Date').text)
        day_number = int(_date.split('-')[2])
        nurse_id = str(shift_off.find('EmployeeID').text)
        weight = int(shift_off.attrib['weight'])
        shift_id = str(shift_off.find('ShiftTypeID').text)

        shift_off_requests.append([day_number, shift_id, nurse_id, weight])

    
    return {
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
    