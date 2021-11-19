from time import sleep
import grpc
import bank_pb2
import bank_pb2_grpc

class Customer:
    def __init__(self, id, events):
        self.id = id
        self.events = events

    def createStub(self, num):
        
        host = 'localhost:' + str(50050 + num)
        channel = grpc.insecure_channel(host)
        stub = bank_pb2_grpc.BankStub(channel)
        return stub

    def executeEvents(self):
        responses = []
        for event in self.events:
            # dynamic stub creation based on the dest value of the event
            stub = self.createStub(event.dest)
            interface = event.interface
            if(interface == 'withdraw'):
                money = event.money
                response = stub.Withdraw(bank_pb2.GeneralRequest(interface='withdraw', money=int(money)))
            if(interface == 'deposit'):
                money = event.money
                response = stub.Deposit(bank_pb2.GeneralRequest(interface='deposit', money=int(money)))
            if(interface == 'query'):
                # stops the process from reading branches that have not been written yet
                sleep(3)
                data = {}
                response = stub.Query(bank_pb2.QueryRequest(id=str(self.id), money=0))
                data['id'] = self.id
                data['balance'] = response.money
                responses.append(data)
        return responses

