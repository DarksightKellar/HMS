class Shift():

    def __init__(self, index, shift_type, n_nurses_required, skills_required, evaluation_multiplier=1, weight=1):
        self.index = index
        self.shift_type = shift_type
        self.n_nurses_required = n_nurses_required
        self.skills_required = skills_required
        self.evaluation_multiplier = evaluation_multiplier
        self.weight = weight
        self.assignment_difficulty = 1
        self.assigned_nurses = []

    def evaluate(self):
        assignment_difficulty = self.weight * self.evaluation_multiplier
        self.assignment_difficulty = assignment_difficulty
        return assignment_difficulty
