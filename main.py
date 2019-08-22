# java -jar data/evaluate.jar -p data/test.xml -s data/test_solution.xml
from instance import *
from hsa import HarmonySearch


# 1. Initialise problem and params
print('\nSetting up Problem Instance...\n')
instance = Instance.create_test_instance()

hsa = HarmonySearch()

# 2. Initialise HM
print('Initialising Harmony Memory...')
hsa.setup(instance)

print(' [DONE]\n\nInitial harmony memory costs:')
print([c[1] for c in hsa.harmony_memory])

print('\nRunning algorithm')
n_runs = 0
while hsa.check_stop_criterion():
    # 3. Improvise new Harmony
    new_harmony = hsa.improvise_harmony()
    
    # 4. Update harmony memory
    hsa.update_memory([schedule.copy() for schedule in new_harmony])
    n_runs += 1

    if n_runs%1000 == 0:
        print(".", end = '')

print(' [DONE]\n\nFinal harmony memory costs:')
print([c[1] for c in hsa.harmony_memory])

print(str.format('\n\n{} iterations', n_runs))