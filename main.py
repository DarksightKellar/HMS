# java -jar data/evaluate.jar -p data/test.xml -s data/test_solution.xml
from instance import *
from hsa import HarmonySearch

print('Setting up instance...')

# 1. Initialise problem and params
instance = Instance.create_test_instance()

print('setting up Harmony Search...')
hsa = HarmonySearch()

# 2. Initialise HM
hsa.setup(instance)

# 3. Improvise new Harmony
new_harmony = hsa.improvise_harmony()

print('done')
from helper_classes.evaluate import evaluate_solution
cost = evaluate_solution(new_harmony, hsa.instance.shifts)
print(cost)