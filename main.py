# java -jar data/evaluate.jar -p data/test.xml -s data/test_solution.xml
from instance import *
from hsa import HarmonySearch

print('Setting up instance...')

# 1. Initialise problem and params
instance = Instance.create_test_instance()

hsa = HarmonySearch()

# 2. Initialise HM
print('setting up Harmony Search...')
hsa.setup(instance)

while hsa.check_stop_criterion():
    # 3. Improvise new Harmony
    print('Improvising new harmony...')
    new_harmony = hsa.improvise_harmony()
    
    # 4. Update harmony memory
    print('Updating harmony memory...')
    hsa.update_memory([schedule.copy() for schedule in new_harmony])

print('done')
from helper_classes.evaluate import evaluate_solution
cost = evaluate_solution(new_harmony, hsa.instance.shifts)
print(cost)