import grpc
import bank_pb2
import bank_pb2_grpc
import time
from concurrent import futures
from google.protobuf import message

class Branch(bank_pb2_grpc.BankServicer):

    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = self.CreateStubs(self.branches)

    def Deposit(self, request, context):
        self.balance += int(request.money)
        # notifies other branches of updates
        for stub in self.stubList:
            stub.BranchDeposit(bank_pb2.BranchRequest(money=request.money))
        return bank_pb2.GeneralReply(interface='deposit', result= 'success')

    def Withdraw(self, request, context):
        self.balance -= request.money
        # notifies other branches of updates
        for stub in self.stubList:
            stub.BranchWithdraw(bank_pb2.BranchRequest(money=request.money))
        return bank_pb2.GeneralReply(interface='withdraw', result= 'success')

    def Query(self, request, context):
        time.sleep(3)
        return bank_pb2.QueryReply(interface='query', result='success', money=self.balance)

    def BranchDeposit(self, request, context):
        self.balance += int(request.money)
        return bank_pb2.BranchResponse(message='success')

    def BranchWithdraw(self, request, context):
        self.balance -= request.money
        return bank_pb2.BranchResponse(message='success')

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