import sys
import os



protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)
import clientServer_pb2_grpc, clientServer_pb2
import grpc
import time


serverDirection="localhost"
def run():
    with grpc.insecure_channel(f'{serverDirection}:50051') as channel:
        stub = clientServer_pb2_grpc.ClientServerStub(channel)
        hello_request=clientServer_pb2.registerRequest(user=input('Please enter the user: '), password=input('Please enter your password: '))
        hello_response= stub.register(hello_request)
        print(hello_response.response)
if __name__ == '__main__':
    run()
        