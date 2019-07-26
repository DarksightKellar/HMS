from shift import Shift


class Nurse():

    def __init__(self, id, last_name, other_names, skills, n_allocations, max_assignments):
        self.id = id
        self.last_name = last_name
        self.other_names = other_names
        self.skills = skills
        self.n_allocations = n_allocations
        self.allocations = [0 for _ in range(n_allocations)]
        self.has_no_allocations = True
        self.max_assignments = max_assignments
        self.n_assignments = 0

    def assign(self, shift: Shift):
        assert(allocation_index < self.n_allocations and allocation_index >= 0)

        self.allocations[shift.index] = 1
        shift.assigned_nurses.append(self)
        self.n_assignments += 1
        self.has_no_allocations = False

    def unassign(self, shift: Shift):
        assert(allocation_index < self.n_allocations and allocation_index >= 0)

        self.allocations[shift.index] = 0
        shift.assigned_nurses.remove(self)
        self.n_assignments -= 1
        self.has_no_allocations = self.n_assignments == 0
