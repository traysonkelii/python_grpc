# seeds the branches created from the input.json file
import json
import threading

from branch import Branch
from types import SimpleNamespace

with open('input.json') as f:
  data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

branches = []
ids = []
for object in data:
    if(object.type == 'branch'):
        branches.append(object)
        ids.append(object.id)

for b in branches:
  b = Branch(b.id, b.balance, ids[:])
  threading.Thread(target=b.StartServer).start()

print('All branches created and listening')
