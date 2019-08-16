import random
from helper_classes.evaluate import evaluate_harmony
from ordering import ordering

from helper_classes.constants import *

HARMONY_MEMORY_CONSIDERATION_RATE = 0.99
PITCH_ADJUSTMENT_RATE = 0.01
N_IMROVISATIONS = 300000 # but quit early after 5000 iterations without improvement
HARMONY_MEMORY_SIZE = 10

class HarmonySearch():
    def __init__(self, HMCR=HARMONY_MEMORY_CONSIDERATION_RATE, PAR=PITCH_ADJUSTMENT_RATE,
                n_improvisations=N_IMROVISATIONS, n_allocations=N_ALLOCATIONS, hm_size=HARMONY_MEMORY_SIZE):
        self.HMCR = HMCR
        self.PAR = PAR
        self.n_improvisations = n_improvisations
        self.n_allocations = n_allocations
        self.hm_size = hm_size

        #  harmony_memory: list of memorised decision variable values
        self.harmony_memory = []

    def setup(self, instance=None, setParams=False, params={}):
        # Extract parameters from the instance
        nurses = instance.nurses
        contracts = instance.contracts
        skills = instance.skills
        shifts = instance.shifts  # set of possible shift types
        period = instance.scheduling_period  # ie, number of days per period
        cover_requests = instance.cover_request_matrix  # is this the demand?
        day_offs = instance.day_off_matrix
        day_ons = instance.day_on_matrix
        shift_offs = instance.shift_off_matrix
        shift_ons = instance.shift_on_matrix

        # number of allocation slots in period
        self.n_allocations = period * len(shifts)

        if setParams:
            self.setParams(params['hmcr'], params['par'],
                params['n_improvisations'], params['hm_size'], params['n_allocations'])

        self.initialise_memory(shifts, nurses)

    def setParams(self, hmcr, par, n_improvisations, hms, n_allocations):
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
        self.n_improvisations = n_improvisations
        self.hm_size = hms
        self.n_allocations = n_vars

    def initialise_memory(self, shifts, nurses):
        '''
        Initialise harmony memory with random solutions
        '''
        
        for i in range(self.hm_size):
            soln_and_cost = ordering(shifts, nurses)
            print('cost', soln_and_cost[1])
            self.harmony_memory.append(soln_and_cost)


    def improvise_harmony(self):
        '''
        Return a newly improvised harmony
        '''
        new_harmony = [[0 for i in range(self.n_allocations)] for _ in range(len(nurs))]

        # for each decision variable...
        for i in range(self.N_DECISION_VARS):
            consider_hm = random.random() <= self.HMCR

            if consider_hm:
                # TODO includes the 'worst' vector in possible selection
                hm_index = random.randint(0, self.HM_SIZE)
                new_harmony[i] = self.harmony_memory[hm_index][i]

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
        worst_cost = evaluate_harmony(self.harmony_memory[self.HM_SIZE])

        if cost < worst_cost:
            self.harmony_memory.append(harmony)

    def check_stop_criterion(self):
        pass
