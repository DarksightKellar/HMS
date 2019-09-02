from math import ceil
from helper_classes.nurse import *
from helper_classes.skills import *
from helper_classes.contract import *

import xml.etree.ElementTree as ET 

def writeXML(destination, instance_name, instance, solution):
    root = ET.Element('Solution')
    period_id = ET.SubElement(root, 'SchedulingPeriodID')
    period_id.text = instance_name
    
    competitor = ET.SubElement(root, 'Competitor')
    competitor.text = 'L. Kelvin'

    n_shifts = len(instance.shift_types)

    employee_i = 1
    for schedule in solution:
        shift_i = 1
        for assigned in schedule:
            if assigned is 0:
                shift_i += 1
                continue
                
            assignment = ET.SubElement(root, 'Assignment')

            date = ET.SubElement(assignment, 'Date')
            day_number = str.format('0{}', shift_i) if shift_i < 10 else shift_i
            date.text = str.format('2010-01-{}', day_number)
            
            employee = ET.SubElement(assignment, 'Employee')
            employee.text = str(employee_i)
            
            shiftType = ET.SubElement(assignment, 'ShiftType')
            shift = instance.shift_types[(shift_i-1) % n_shifts]
            shiftType.text = str(shift)[0]
            
            shift_i += 1

        employee_i += 1

    # create a new XML file with the results
    data = ET.tostring(root)
    with open(destination, 'w') as _dest:
        output = str(data)
        output = output[2:len(output)-1]
        _dest.write(output)
    
    return True
    