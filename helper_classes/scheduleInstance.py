class Schedule():

    def __init__(self, nurses, begin_date, end_date, skills, shifts, contracts, cover_request_matrix,
                day_off_matrix, day_on_matrix, shift_off_matrix, shift_on_matrix):
        self.nurses = nurses
        self.begin_date = begin_date
        self.end_date = end_date
        self.skills = skills
        self.contracts = contracts
        self.cover_request_matrix = cover_request_matrix
        self.day_off_matrix = day_off_matrix
        self.day_on_matrix = day_on_matrix
        self.shift_off_matrix = shift_off_matrix
        self.shift_on_matrix = shift_on_matrix
        self.scheduling_period = (end_date - begin_date).days + 1
