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

    number_of_days = int(root.attrib['nDays'])
    skills = [] 
    shift_types = []
    shift_skills = []
    shift_ids = []
    patterns = []
    contracts = []
    nurses = []
    cover_requirements = []
    day_off_requests = []
    shift_off_requests = []


    # retrieve skills
    for skill in root.findall('./Skills/Skill'):
        skills.append(Skill(skill.text))

    # retrieve shift types, and associated required skills
    for shift in root.findall('./ShiftTypes/Shift'):
        # for shift in st.findall('Shift'):
        shift_types.append(shift.find('Description').text)
        shift_skills.append([Skill(sk.text) for sk in shift.findall('Skills/Skill')])
        shift_ids.append(shift.attrib['ID'])

    # retrieve patterns
    for pattern in root.findall('./Patterns/Pattern'):
        pass

    # retrieve contracts
    for contract in root.findall('./Contracts/Contract'):
        min_total = contract.find('MinNumAssignments').text
        max_total = contract.find('MaxNumAssignments').text

        min_consecutive = contract.find('MinConsecutiveWorkingDays').text
        max_consecutive = contract.find('MaxConsecutiveWorkingDays').text
        
        min_between = contract.find('MinConsecutiveFreeDays').text
        max_between = contract.find('MaxConsecutiveFreeDays').text

        contracts.append(Contract(
            limit_total=[min_total, max_total],
            limit_consecutive=[min_consecutive, max_consecutive],
            limit_between=[min_between, max_between],
        ))

    # retrieve nurses
    for n in root.findall('./Employees/Employee'):
        names = str(n.find('Name').text).split(' ')
        nurse_skills = [ Skill(sk.text) for sk in n.find('Skills') ]
        contract_id = int(n.find('ContractID').text)
        nurse_id = str(n.attrib['ID'])

        nurse = Nurse(
            id, names[len(names)-1], names[0:len(names)-1], 
            nurse_skills, 5, contracts[contract_id], nurse_id=nurse_id
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
        'patterns': patterns,
        'contracts': contracts,
        'nurses': nurses,
        'cover_requirements': cover_requirements,
        'day_off_requests': day_off_requests,
        'shift_off_requests': shift_off_requests
    }
    