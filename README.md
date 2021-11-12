# Logical Clock Lab

This lab was implemented via `python 3.8.5`. 

## How to use
- Place a formatted json file named `input.json` in the root directory (note that one is already provided in this repository). The json object should contain an equal number of customer and branch processes. There should be a one to one mapping between `customer id` and `branch id`. All starting `balance`'s of any `branch` referenced should be the same amount upon starting the application. (example can be found below)
- run the following sequences of python commands from the root directory to execute the program to initialize the branches:
```
# generates the pb2 files
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bank.proto

# dynamically creates the branches on separate ports
python create_branches.py
```
(on a separate terminal run the following command)
```
python execute_input.py
```
- Upon completion an `output.json` will be generated with  the logical clock representation (partitioned between the processes and the events of a given client request).

## Example Input
```
[{ 'id': 1, 'type': 'customer',
    events: [
        { 'id': 1, interface: 'query', money: 400 }
    ]},
  { 'id': 2, 'type': 'customer',
    'events': [
        { 'id': 2, 'interface': 'deposit', 'money': 170 },
        { 'id': 3, 'interface': 'query', 'money': 400 }
    ]},
  { 'id': 3, 'type': 'customer',
    'events': [
      { 'id': 4, 'interface': 'withdraw', 'money': 70 },
      { 'id': 5, 'interface': 'query', 'money': 400 }
    ]},
  { 'id': 1, 'type': 'branch', 'balance': 400 },
  { 'id': 2, 'type': 'branch', 'balance': 400 },
  { 'id': 3, 'type': 'branch', 'balance': 400}]
```

## Example Output
```
[
    {
      "pid": 1,
      "data": [
        { "id": 4, "name": "withdraw_propagate_request", "clock": 4 },
        { "id": 4, "name": "withdraw_propagate_execute", "clock": 5 },
        { "id": 2, "name": "deposit_propagate_request", "clock": 6 },
        { "id": 2, "name": "deposit_propagate_execute", "clock": 7 }
      ]
    },
    {
      "pid": 2,
      "data": [
        { "id": 2, "name": "deposit_request", "clock": 2 },
        { "id": 2, "name": "deposit_execute", "clock": 3 },
        { "id": 2, "name": "deposit_propagate_response", "clock": 8 },
        { "id": 4, "name": "withdraw_propagate_request", "clock": 9 },
        { "id": 4, "name": "withdraw_propagate_execute", "clock": 10 },
        { "id": 2, "name": "deposit_propagate_response", "clock": 15 },
        { "id": 2, "name": "deposit_response", "clock": 16 }
      ]
    },
    {
      "pid": 3,
      "data": [
        { "id": 4, "name": "withdraw_request", "clock": 2 },
        { "id": 4, "name": "withdraw_execute", "clock": 3 },
        { "id": 4, "name": "withdraw_propagate_response", "clock": 6 },
        { "id": 4, "name": "withdraw_propagate_response", "clock": 11 },
        { "id": 4, "name": "withdraw_response", "clock": 12 },
        { "id": 2, "name": "deposit_propagate_request", "clock": 13 },
        { "id": 2, "name": "deposit_propagate_execute", "clock": 14 }
      ]
    },
    {
      "eventId": 4,
      "data": [
        { "clock": 2, "name": "withdraw_request" },
        { "clock": 3, "name": "withdraw_execute" },
        { "clock": 4, "name": "withdraw_propagate_request" },
        { "clock": 5, "name": "withdraw_propagate_execute" },
        { "clock": 6, "name": "withdraw_propagate_response" },
        { "clock": 9, "name": "withdraw_propagate_request" },
        { "clock": 10, "name": "withdraw_propagate_execute" },
        { "clock": 11, "name": "withdraw_propagate_response" },
        { "clock": 12, "name": "withdraw_response" }
      ]
    },
    {
      "eventId": 2,
      "data": [
        { "clock": 2, "name": "deposit_request" },
        { "clock": 3, "name": "deposit_execute" },
        { "clock": 6, "name": "deposit_propagate_request" },
        { "clock": 7, "name": "deposit_propagate_execute" },
        { "clock": 8, "name": "deposit_propagate_response" },
        { "clock": 13, "name": "deposit_propagate_request" },
        { "clock": 14, "name": "deposit_propagate_execute" },
        { "clock": 15, "name": "deposit_propagate_response" },
        { "clock": 16, "name": "deposit_response" }
      ]
    }
  ]
  
```

## Output disparity

Note that running this command multiple times will produce different results mainly due to the race conditions implemented in the aggregation step of the client calls. While the output may not have all the logical ticks recorded by a certain process, the sequential nature and integrity of the global clock is preserved. View an example of an output missing data below:

```
[
    {
      "pid": 1,
      "data": [
        { "id": 4, "name": "withdraw_propagate_request", "clock": 4 },
        { "id": 4, "name": "withdraw_propagate_execute", "clock": 5 },
        { "id": 2, "name": "deposit_propagate_request", "clock": 6 },
        { "id": 2, "name": "deposit_propagate_execute", "clock": 7 }
      ]
    },
    {
      "pid": 2,
      "data": [
        { "id": 2, "name": "deposit_request", "clock": 2 },
        { "id": 2, "name": "deposit_execute", "clock": 3 },
        { "id": 2, "name": "deposit_propagate_response", "clock": 8 },
        { "id": 4, "name": "withdraw_propagate_request", "clock": 9 },
        { "id": 4, "name": "withdraw_propagate_execute", "clock": 10 },
        { "id": 2, "name": "deposit_propagate_response", "clock": 15 },
        { "id": 2, "name": "deposit_response", "clock": 16 }
      ]
    },
    {
      "pid": 3,
      "data": [
        { "id": 4, "name": "withdraw_request", "clock": 2 },
        { "id": 4, "name": "withdraw_execute", "clock": 3 },
        { "id": 4, "name": "withdraw_propagate_response", "clock": 6 },
        { "id": 4, "name": "withdraw_propagate_response", "clock": 11 },
        { "id": 4, "name": "withdraw_response", "clock": 12 }
      ]
    },
    {
      "eventId": 4,
      "data": [
        { "clock": 2, "name": "withdraw_request" },
        { "clock": 3, "name": "withdraw_execute" },
        { "clock": 4, "name": "withdraw_propagate_request" },
        { "clock": 5, "name": "withdraw_propagate_execute" },
        { "clock": 6, "name": "withdraw_propagate_response" },
        { "clock": 9, "name": "withdraw_propagate_request" },
        { "clock": 10, "name": "withdraw_propagate_execute" },
        { "clock": 11, "name": "withdraw_propagate_response" },
        { "clock": 12, "name": "withdraw_response" }
      ]
    },
    {
      "eventId": 2,
      "data": [
        { "clock": 2, "name": "deposit_request" },
        { "clock": 3, "name": "deposit_execute" },
        { "clock": 6, "name": "deposit_propagate_request" },
        { "clock": 7, "name": "deposit_propagate_execute" },
        { "clock": 8, "name": "deposit_propagate_response" },
        { "clock": 15, "name": "deposit_propagate_response" },
        { "clock": 16, "name": "deposit_response" }
      ]
    }
  ]
```