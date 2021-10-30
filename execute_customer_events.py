# runs the customer events specified in input.json and writes the responses to output.json
import json
from threading import Thread
from types import SimpleNamespace
from customer import Customer

with open('input.json') as f:
  data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

customers = []
for object in data: 
  if(object.type == 'customer'):
    customers.append(object)

# creates threads equal to amonut of customer, run individually
threads = [None] * len(customers)
# creates results to perserve order
results = [None] * len(customers)

def executeCustomer(data, i):
  customer = Customer(data.id, data.events)
  results[i] = customer.executeEvents()

# each thread runs on it's own process to handle query sleep (non-blocking)
for i in range(len(customers)):
  threads[i] = Thread(target=executeCustomer, args=(customers[i], i))
  threads[i].start()

# collects threads upon completion
for i in range(len(threads)):
  threads[i].join()

output = []
for i in range(len(results)):
  result = {}
  # offset due to zero indexing
  result['id'] = i+1
  result['recv'] = results[i]
  output.append(result)
  with open('output.json', 'w') as outfile:
    json.dump(output, outfile)

print("All customer events have been executed, look for output.json")