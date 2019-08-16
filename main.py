# java -jar data/evaluate.jar -p data/test.xml -s data/test_solution.xml
from instance import *
from hsa import HarmonySearch

print('Setting up instance...')

instance = Instance.create_test_instance()

print('setting up Harmony Search...')
hsa = HarmonySearch()
hsa.setup(instance)
print('done')