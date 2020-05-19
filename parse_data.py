import json

from data import *

with open('./db/goals.json', 'w+') as f:
    f.write(json.dumps(goals))

with open('./db/week.json', 'w+') as f:
    f.write(json.dumps(week))

with open('./db/hours.json', 'w+') as f:
    f.write(json.dumps(hours))

with open('./db/teachers.json', 'w+') as f:
    f.write(json.dumps(teachers))
