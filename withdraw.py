import grpc
import sys
import bank_pb2_grpc
import bank_pb2

port=sys.argv[1]
money=sys.argv[2]
host = 'localhost:'+str(port)
channel = grpc.insecure_channel(host)
stub = bank_pb2_grpc.BankStub(channel)
response = stub.Withdraw(bank_pb2.GeneralRequest(interface='withdraw', money=int(money)))
print("\nWithdraw from server: " + response.result) 