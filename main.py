# java -jar data/evaluate.jar -p data/test.xml -s data/test_solution.xml
from instance import *
from hsa import HarmonySearch
from test_instances import create_instance

from helper_classes.evaluate import *


# 1. Initialise problem and params
print('\nSetting up Problem Instance...\n')
# instance = Instance.create_test_instance()
_instance = create_instance()
instance = _instance

hsa = HarmonySearch(n_allocations=instance.nurses[0].n_allocations)

# 2. Initialise HM
print('Initialising Harmony Memory...')
hsa.setup(instance)

print(' [DONE]\n\nInitial harmony memory costs:')
print([c[1] for c in hsa.harmony_memory])

print('\nRunning algorithm')
while hsa.check_stop_criterion():
    # 3. Improvise new Harmony
    new_harmony = hsa.improvise_harmony()
    
    # 4. Update harmony memory
    hsa.update_memory(new_harmony)#[schedule.copy() for schedule in new_harmony])

    if hsa.improvisations_done%1000 == 0:
        print(".", end = '', flush=True)

print(' [DONE]\n\nFinal harmony memory costs:')
print([c[1] for c in hsa.harmony_memory])

print(str.format('\n\n{} iterations', hsa.improvisations_done))
print(str.format('\n{} infeasible solutions found', hsa.n_infeasible_solutions))

best_solution = hsa.harmony_memory[0]
for x in hsa.harmony_memory:
    if x[1] < best_solution[1]:
        best_solution = x

# cost = evaluate_harmony(best_solution[0], instance)

print('')