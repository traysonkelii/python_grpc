# gRPC Lab

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
python execute_customer_events.py
```
- Upon completion an `output.json` will be generated and with the corresponding transaction status

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
{'id': 1, 'recv': [{'interface': 'query', 'result': 'success', 'money': 500}]}
  {'id': 2, 'recv': [{'interface': 'deposit', 'result': 'success'}, {'interface': 'query', 'result': 'success', 'money': 500}]}
  {'id': 3, 'recv': [{'interface': 'withdraw', 'result': 'success'}, {'interface': 'query', 'result': 'success', 'money': 500}]}
```

## Extra Testing

After running `python execute_customer_events.py` you can further test the individual operations (Withdraw, Deposit, and Query) by executing the following commands (note that the specific setup defined for the input.json will be `50051`, `50052`, and `50053`): 

Withdraw
```
python withdraw.py [PORT] [AMOUNT_TO_WITHDRAW]
```

Deposit
```
python withdraw.py [PORT] [AMOUNT_TO_DEPOSIT]
```

Query
```
python withdraw.py [PORT] [PLACE_HOLDER_AMOUNT]
```