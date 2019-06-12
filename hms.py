import random
from evaluate import evaluate_harmony
from ordering import ordering


class HarmonySearch():
    # number of decision variables (instruments, in this case, nurse 0-1 assignment values for scheduling period)
    N_DECISION_VARS = 5
    HMCR = 0.1  # Harmony Memory Consideration Rate
    PAR = 0.1  # Pitch Adjustment Rate
    N_IMROVISATIONS = 1000
    N_ALLOCATIONS = 90  # 30-day period, 3 shifts per day

    #  harmony_memory: list of memorised decision variable values
    HARMONY_MEMORY = []
    HM_SIZE = 0

    # all possible pitches for each decision variable
    # format: [ [1, 6, 9], [8, 19, 20, 60] ]
    # size: N_DECISION_VARS
    # TODO - this needs to be initialised somehow (does it tho??)
    HARMONY_SPACE = []

    def hms(self, instance=None, setParams=False, params=[]):
        # Extract parameters from the instance

        # _x: N-dimensional vector of decision variables
        # K: N-dimensional vector of number of possible
        #    values of each decision variable
        # X: N-sized list of possible values of _x
        # K(i): number of possible vals of x(i)
        # X(i): K(i)-sized list of all possible discrete
        #        vals of each decision variable, x(i)

        instance.nurses
        instance.contracts
        instance.skills
        instance.shifts  # a set; get number by counting
        instance.scheduling_period  # ie, number of days per period
        instance.cover_request_matrix  # is this the demand?
        instance.day_off_matrix
        instance.day_on_matrix
        instance.shift_off_matrix
        instance.shift_on_matrix

        # number of allocation slots in period
        self.N_ALLOCATIONS = instance.scheduling_period * len(instance.shifts)

        if setParams:
            self.setParams(params['hmcr'], params['par'],
                           params['ni'], params['hms'], params['n_vars'])

        self.initialise_memory()

        for _ in range(self.N_IMROVISATIONS):
            new_harmony = self.improvise_harmony()
            self.update_memory(new_harmony)

    def setParams(self, hmcr, par, ni, hms, n_vars):
        '''
        set algorithm params:-
         hmcr: used to decide next source of decision variable value;
               from harmory_memory or select randomly from X
         par: pitch adjustment rate; used to decide when to adjust
              decision variable to neighbouring value
         ni: number of improvisations to be done
         hms: size of harmony memory
         n_vars: number of decision variables
        '''
        self.HMCR = hmcr
        self.PAR = par
        self.N_IMROVISATIONS = ni
        self.HM_SIZE = hms
        self.N_DECISION_VARS = n_vars

    def initialise_memory(self):
        '''
        Initialise harmony memory with zeros
        '''

        # Construct pool of feasible solutions:
        #

        # 0-1 list indicating assignment or not (initially all not assigned)
        allocations = [0 for _ in range(self.N_ALLOCATIONS)]

        # duplicate unassigned allocations for each nurse to form one solution
        solution = [allocations for _ in range(self.N_DECISION_VARS)]

        # duplicate solutions for each slot in harmony memory
        self.HARMONY_MEMORY = [solution for _ in range(self.HM_SIZE)]

        # ensure all solutions in harmony memory are feasible

    def improvise_harmony(self):
        '''
        Return a newly improvised harmony
        '''
        new_harmony = [0 for i in range(self.N_DECISION_VARS)]

        # for each decision variable...
        for i in range(self.N_DECISION_VARS):
            consider_hm = random.random() <= self.HMCR

            if consider_hm:
                # TODO includes the 'worst' vector in possible selection
                hm_index = random.randint(0, self.HM_SIZE)
                new_harmony[i] = self.HARMONY_MEMORY[hm_index][i]

                adjust_pitch = random.random() <= self.PAR
                if adjust_pitch:
                    # TODO how to adjust pitch
                    new_harmony[i] = self.HARMONY_SPACE[i]
            else:
                # Pick a random pitch from the harmony space,
                # which has format: [ [1, 6, 9], [8, 19, 20, 60] ]
                for i in range(self.N_DECISION_VARS):
                    possible_vals = self.HARMONY_SPACE[i]
                    val_index = random.randint(0, possible_vals.count())

                    new_harmony[i] = possible_vals[val_index]

        return new_harmony

    def update_memory(self, harmony):
        cost = evaluate_harmony(harmony)
        worst_cost = evaluate_harmony(self.HARMONY_MEMORY[self.HM_SIZE])

        if cost < worst_cost:
            self.HARMONY_MEMORY.append(harmony)

    def check_stop_criterion(self):
        pass
