from helper_classes.shift import Shift
from helper_classes.constants import *

class Nurse():

    def __init__(self, id, last_name, other_names, skills, contract=None, nurse_id=None, n_allocations=N_ALLOCATIONS):
        self.id = id
        self.last_name = last_name
        self.other_names = other_names
        self.skills = skills
        self.n_allocations = n_allocations
        self.allocations = [0 for _ in range(n_allocations)]
        self.has_no_allocations = True
        self.n_assignments = 0
        self.contract = contract
        self.nurse_id = nurse_id

    def assign(self, shift: Shift):
        assert(shift.index < self.n_allocations and shift.index >= 0)

        self.allocations[shift.index] = 1

        if self not in shift.assigned_nurses:
            shift.assigned_nurses.append(self)
            self.n_assignments += 1
            self.has_no_allocations = False

    def unassign(self, shift: Shift):
        assert(shift.index < self.n_allocations and shift.index >= 0)

        self.allocations[shift.index] = 0
        shift.assigned_nurses.remove(self)
        self.n_assignments -= 1
        self.has_no_allocations = self.n_assignments == 0

    def duplicate(self):
        return Nurse(id, self.last_name, self.other_names, self.skills, self.contract, self.nurse_id, self.n_allocations)