""" 
Study Session Logger 
Uses Forgetting Curve + Spaced Repetation 
"""

import json 
import math
import os 

from datetime import datetime, timedelta 

data_file = "study_ses.json"

