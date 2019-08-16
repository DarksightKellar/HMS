import random
from helper_classes.evaluate import *
from ordering import ordering

from helper_classes.constants import *

HARMONY_MEMORY_CONSIDERATION_RATE = 0.99
PITCH_ADJUSTMENT_RATE = 0.5
N_IMROVISATIONS = 10
PLATEAU_THRESHOLD = 5 # but quit early after this number of iterations without improvement
HARMONY_MEMORY_SIZE = 8

class HarmonySearch():
    def __init__(self, HMCR=HARMONY_MEMORY_CONSIDERATION_RATE, PAR=PITCH_ADJUSTMENT_RATE,
                n_improvisations=N_IMROVISATIONS, n_allocations=N_ALLOCATIONS, hm_size=HARMONY_MEMORY_SIZE):
        self.HMCR = HMCR
        self.PAR = PAR
        self.n_improvisations = n_improvisations
        self.n_allocations = n_allocations
        self.hm_size = hm_size
        self.improvisations_done = 0
        self.n_improvisations_without_improvement = 0

        # harmony_memory: list of memorised decision variable values, 
        # with costs: [soln, cost]
        self.harmony_memory = []

    def setup(self, instance=None, setParams=False, params={}):
        # Extract parameters from the instance
        nurses = instance.nurses
        contracts = instance.contracts
        skills = instance.skills
        shifts = instance.shifts
        shift_types = instance.shift_types  # set of possible shift types
        period = instance.scheduling_period  # ie, number of days per period
        cover_requests = instance.cover_request_matrix  # is this the demand?
        day_offs = instance.day_off_matrix
        day_ons = instance.day_on_matrix
        shift_offs = instance.shift_off_matrix
        shift_ons = instance.shift_on_matrix

        if setParams:
            self.setParams(params['hmcr'], params['par'],
                params['n_improvisations'], params['hm_size'], params['n_allocations'])

        self.initialise_memory(shifts, nurses)
        self.instance = instance

    def setParams(self, hmcr, par, n_improvisations, hms, n_allocations):
        '''
        set algorithm params:-
        hmcr: used to decide next source of decision variable value;
            from harmory_memory or select randomly from X
        par: pitch adjustment rate; used to decide when to adjust
            decision variable to neighbouring value
        n_improvisations: number of improvisations to be done
        hms: size of harmony memory
        n_allocations: number of decision variables
        '''
        self.HMCR = hmcr
        self.PAR = par
        self.n_improvisations = n_improvisations
        self.hm_size = hms
        self.n_allocations = n_allocations

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
        new_harmony = [[0 for _ in range(self.n_allocations)] for _ in range(len(self.instance.nurses))]
        
        # List of scheduled nurses (instruments that played new improvisation from HM)
        already_scheduled_idxs = []


        # for each instrument (ie nurse), generate new improvisation ...
        for instrument_i in range(len(self.instance.nurses)):
            consider_hm = random.random() <= self.HMCR

            if consider_hm:
                hm_index = random.randint(0, self.hm_size-1)
                [rand_soln, cost] = self.harmony_memory[hm_index]

                schedule = rand_soln[instrument_i]
                new_harmony[instrument_i] = schedule
                
                already_scheduled_idxs.append(instrument_i)

                # Possibly adjust pitch
                rand = random.random()
                adjust_pitch = rand <= self.PAR
                if adjust_pitch:
                    PAR1 = self.PAR/3
                    PAR2 = 2 * self.PAR/3
                    PAR3 = self.PAR

                    move = rand < PAR1
                    swap_nurses = PAR1 <= rand and rand < PAR2
                    swap_days = PAR2 <= rand and rand < PAR3
                    
                    # get indices of free (as yet unscheduled) instruments
                    free_idxs = []
                    for idx in range(len(new_harmony)):
                        if idx not in already_scheduled_idxs:
                            free_idxs.append(idx)

                    if move and len(free_idxs != 0):
                        # randomly select a free instrument
                        rand_free_idx = random.sample(free_idxs, 1)[0]
                        selected_instrument = new_harmony[rand_free_idx]
                        
                        # move the schedule (ie decision variable values)
                        # to this instrument
                        new_harmony[rand_free_idx] = schedule
                        new_harmony[instrument_i] = selected_instrument

                        already_scheduled_idxs.remove(instrument_i)
                        
                    if swap_nurses:
                        # randomly select a scheduled instrument
                        rand_scheduled_idx = random.sample(already_scheduled_idxs, 1)[0]
                        selected_instrument = new_harmony[rand_scheduled_idx]
                        
                        # swap the schedule with this instrument
                        new_harmony[instrument_i] = selected_instrument
                        new_harmony[rand_scheduled_idx] = schedule

                    if swap_days:
                        from math import ceil

                        # select random assigned day in the schedule
                        indx = random.randint(0, self.n_allocations-1)
                        while schedule[indx] is not 1:
                            indx = random.randint(0, self.n_allocations-1)

                        day_number = ceil((indx+1) / N_SHIFTS)

                        # select random scheduled nurse
                        rand_scheduled_idx = random.sample(already_scheduled_idxs, 1)[0]
                        selected_instrument = new_harmony[rand_scheduled_idx]

                        # select random assigned day in schedule of selected instrument
                        # that is also on a day different from that selected from schedule
                        sel_indx = random.randint(0, self.n_allocations-1)
                        sel_day_number = ceil((sel_indx+1) / N_SHIFTS)

                        while selected_instrument[sel_indx] is not 1 or day_number is sel_day_number:
                            sel_indx = random.randint(0, self.n_allocations-1)
                            sel_day_number = ceil((sel_indx+1) / N_SHIFTS)

                        # Now swap the assignments for these days
                        schedule[sel_indx] = 1
                        schedule[indx] = 0

                        selected_instrument[sel_indx] = 0
                        selected_instrument[indx] = 1    

            # else: # randomise instrument decision vars
            #     for decision_var_i in range(self.n_allocations):
            #         # RESEARCH POINT: tend these assignements toward improving cost
            #         # (means I'll have to rather track instruments for which HM wasn't 
            #         # considered,then for each, attempt setting decision variables)
            #         new_harmony[instrument_i][decision_var_i] = random.randint(0, 1)

        self.improvisations_done += 1
        
        return new_harmony

    def update_memory(self, harmony):
        cost = evaluate_solution(harmony, self.instance.shifts)

        if cost is None:
            return

        # get memorised soln with worst cost
        worst_soln_cost = [[], 0]
        for soln_cost in self.harmony_memory:
            if soln_cost[1] > worst_soln_cost[1]:
                worst_soln_cost = soln_cost

        if cost < worst_soln_cost[1]:
            self.harmony_memory.remove(worst_soln_cost)
            self.harmony_memory.append([harmony, cost])
            self.n_improvisations_without_improvement = 0
        else:
            self.n_improvisations_without_improvement += 1

    def check_stop_criterion(self):
        '''
        Check that the algorithm can continue to improvise.
        
        Returns `True` if the algorithm should continue, `False` if it should terminate
        '''
        if self.improvisations_done == self.n_improvisations:
            return False

        if self.n_improvisations_without_improvement > PLATEAU_THRESHOLD:
            return False

        return True
            
