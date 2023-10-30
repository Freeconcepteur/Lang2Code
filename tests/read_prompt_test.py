import sys, os
sys.path.append(os.path.dirname(__file__) + "/..")
from database_operations.db_utilities import read_prompts

    

print(read_prompts())
