from tests.db_utilities import read_prompts
import sys
import os
sys.path.append(os.path.dirname(__file__) + "/..")


print(read_prompts())
