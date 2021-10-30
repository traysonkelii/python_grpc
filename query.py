import bank_pb2_grpc
import bank_pb2
import grpc
import sys

port=sys.argv[1]
money=sys.argv[2]
host = 'localhost:'+str(port)
channel = grpc.insecure_channel(host)
stub = bank_pb2_grpc.BankStub(channel)
response = stub.Query(bank_pb2.GeneralRequest(interface='query', money=int(money)))
print("\nQuery from server: " + response.result + " " + str(response.money))