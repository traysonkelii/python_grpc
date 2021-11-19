# gRPC Lab

This lab was implemented via `python 3.8.5`. 

## How to use
- Place a formatted json file named `input.json` in the root directory (note that one is already provided in this repository). All starting `balance`'s of any `branch` referenced should be the same amount upon starting the application. (example can be found below)
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
[
  {
    "id": 1,
    "type": "customer",
    "events": [
      { "interface": "deposit", "money": 400, "dest": 1 },
      { "interface": "query", "dest": 2 }
    ]
  },
  {
    "id": 1,
    "type": "bank",
    "balance": 0
  },
  {
    "id": 2,
    "type": "bank",
    "balance": 0
  }
]

```

## Example Output
```
[{"id": 1, "balance": 400}]
```

## Extra Testing

After running `python create_branches.py` you can further test the individual operations (Withdraw, Deposit, and Query) by executing the following commands (note that the specific setup defined for the input.json will be `50051`, `50052`, and `50053`): 

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