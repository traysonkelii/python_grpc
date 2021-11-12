import grpc
import bank_pb2
import bank_pb2_grpc
import time
from concurrent import futures

class Branch(bank_pb2_grpc.BankServicer):

    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = self.CreateStubs(self.branches)
        self.clock = 0
        self.executions = []

    def Deposit(self, request, context):
        # Event_Request
        self.clock = max(self.clock, request.clock) + 1
        self.executions.append({"id": request.id, "name": "deposit_request", "clock": self.clock})

        # Event_Execute
        self.balance += int(request.money)
        self.clock += 1
        self.executions.append({"id": request.id, "name": "deposit_execute", "clock": self.clock})

        for stub in self.stubList:
            #Propagate_Request
            fellow = stub.BranchDeposit(bank_pb2.BranchRequest(money=request.money, clock=self.clock, id=request.id))

            # Propagate_Response 
            self.clock = max(self.clock, fellow.clock) + 1
            self.executions.append({"id": request.id, "name": "deposit_propagate_response", "clock": self.clock})

        # Event_Response 
        self.clock += 1
        self.executions.append({"id": request.id, "name": "deposit_response", "clock": self.clock})
        return bank_pb2.GeneralReply(interface='deposit', result= 'success', executions=str(self.executions))

    def Withdraw(self, request, context):
        # Event_Request
        self.clock = max(self.clock, request.clock) + 1
        self.executions.append({"id": request.id, "name": "withdraw_request", "clock": self.clock})

        # Event_Request
        self.balance -= request.money
        self.clock += 1
        self.executions.append({"id": request.id, "name": "withdraw_execute", "clock": self.clock})
   
        for stub in self.stubList:
            fellow = stub.BranchWithdraw(bank_pb2.BranchRequest(money=request.money, clock=self.clock, id=request.id))
            
            # Propagate_Response 
            self.clock = max(self.clock, fellow.clock) + 1
            self.executions.append({"id": request.id, "name": "withdraw_propagate_response", "clock": self.clock})

        # Event_Response 
        self.clock += 1
        self.executions.append({"id": request.id, "name": "withdraw_response", "clock": self.clock})
        return bank_pb2.GeneralReply(interface='withdraw', result= 'success', executions=str(self.executions))

    def BranchDeposit(self, request, context):
        #Propagate_Request     
        self.clock = max(self.clock, request.clock) + 1
        self.executions.append({"id": request.id, "name": "deposit_propagate_request", "clock": self.clock})
        self.balance += int(request.money)
        
        #Propagate_Execute     
        self.clock += 1
        self.executions.append({"id": request.id, "name": "deposit_propagate_execute", "clock": self.clock})
        return bank_pb2.BranchResponse(message='success', clock=self.clock, executions=str(self.executions))

    def BranchWithdraw(self, request, context):
        #Propagate_Request     
        self.clock = max(self.clock, request.clock) + 1
        self.executions.append({"id": request.id, "name": "withdraw_propagate_request", "clock": self.clock})
        self.balance -= request.money

        #Propagate_Execute     
        self.clock += 1
        self.executions.append({"id": request.id, "name": "withdraw_propagate_execute", "clock": self.clock})
        return bank_pb2.BranchResponse(message='success', clock=self.clock, executions=str(self.executions))

    def Query(self, request, context):
        time.sleep(3)
        return bank_pb2.QueryReply(interface='query', result='success', money=self.balance, executions=str(self.executions))

    def CreateStubs(self, branches):
        stubs = []
        branches.remove(self.id)
        for branch in branches:
            # simple mapping of id to port
            port = 50050 + branch
            channel = grpc.insecure_channel('localhost:'+str(port))
            stub = bank_pb2_grpc.BankStub(channel)
            stubs.append(stub)
        return stubs

    def StartServer(self):
        port = 50050 + self.id
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        bank_pb2_grpc.add_BankServicer_to_server(self, server)
        server.add_insecure_port('[::]:' + str(port))
        server.start()
        # waits open, needs to run on it's own thread to avoid blocking other branches
        server.wait_for_termination()