# runs the customer events specified in input.json and writes the responses to output.json
import json
from threading import Thread
from types import SimpleNamespace
from customer import Customer
from operator import attrgetter

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
execs = []
eventObject = {}
for i in range(len(results)):
  processObject = {}
  processObject['pid'] = i + 1
  processJson = json.loads(results[i][0]['exec'].replace("\'", "\""))
  processObject['data'] = processJson

  for pJson in processJson:
    if pJson['id'] in eventObject:
      eventObject[pJson['id']].append(pJson)
    else:
      eventObject[pJson['id']] = [pJson]
  output.append(processObject)

toAddToOutput = []
for key in eventObject:
  event = {}
  event['eventId'] = key
  event['data'] = []
  for d in eventObject[key]:
    event['data'].append({"clock": d['clock'], "name": d['name']})
  event['data'] = sorted(event['data'], key=lambda k: k['clock']) 
  toAddToOutput.append(event)

with open('output.json', 'w') as outfile:
  json.dump(output + toAddToOutput, outfile)
