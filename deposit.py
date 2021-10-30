import bank_pb2_grpc
import bank_pb2
import grpc
import sys

port=sys.argv[1]
money=sys.argv[2]
host = 'localhost:'+str(port)
channel = grpc.insecure_channel(host)
stub = bank_pb2_grpc.BankStub(channel)
response = stub.Deposit(bank_pb2.GeneralRequest(interface='deposit', money=int(money)))
print("\nDeposit from server: " + response.result) 