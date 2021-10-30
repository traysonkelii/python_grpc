import grpc
import bank_pb2
import bank_pb2_grpc

class Customer:
    def __init__(self, id, events):
        self.id = id
        self.events = events
        # Mapping to proper id
        self.stub = self.createStub()

    def createStub(self):
        # Mapping from self id to Branch id
        host = 'localhost:' + str(50050 + self.id)
        channel = grpc.insecure_channel(host)
        stub = bank_pb2_grpc.BankStub(channel)
        return stub

    # needs to run on it's own thread to handle concurrency
    def executeEvents(self):
        responses = []
        for event in self.events:
            interface = event.interface
            money = event.money
            responses.append(self.commandMapping(interface, money))
        return responses

    def commandMapping(self, interface, money):
        formatted = {}
        if(interface == 'withdraw'):
            response = self.stub.Withdraw(bank_pb2.GeneralRequest(interface='withdraw', money=int(money)))
            formatted['interface'] = response.interface
            formatted['result'] = response.result
        if(interface == 'deposit'):
            response = self.stub.Deposit(bank_pb2.GeneralRequest(interface='deposit', money=int(money)))
            formatted['interface'] = response.interface
            formatted['result'] = response.result
        if(interface == 'query'):
            response = self.stub.Query(bank_pb2.GeneralRequest(interface='query', money=int(money)))
            formatted['interface'] = response.interface
            formatted['result'] = response.result
            formatted['money'] = response.money
        return formatted
