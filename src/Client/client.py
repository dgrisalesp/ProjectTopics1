import sys
import os
import grpc
import time
import threading

# Set up paths for protobuf files
protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)

# Import generated gRPC classes
import clientServer_pb2_grpc, clientServer_pb2, clientDataNode_pb2_grpc, clientDataNode_pb2

# Server direction constant
SERVER_ADDRESS = "54.198.253.100:50051"

class Client:
    def __init__(self):
        self.stub = None
        self.stay_alive_thread = None
        self.stay = False
        self.username = ''
        self.password = ''

    def connect(self):
        channel = grpc.insecure_channel(SERVER_ADDRESS)
        self.stub = clientServer_pb2_grpc.ClientServerStub(channel)

    def staying_alive(self, time_to_live):
        while self.stay:
            stay_request = clientServer_pb2.stayRequest(id=self.username, username=self.username)
            self.stub.stayingAlive(stay_request)
            time.sleep(time_to_live)

    def login(self, user, password):
        login_request = clientServer_pb2.loginRequest(user=user, password=password)
        login_response = self.stub.login(login_request)
        
        if login_response.value == 1:
            self.username = user
            self.password = password
            self.stay = True
            self.stay_alive_thread = threading.Thread(target=self.staying_alive, args=(90,))
            self.stay_alive_thread.start()
        
        return login_response

    def logout(self):
        self.username = ''
        self.password = ''
        self.stay = False
        if self.stay_alive_thread:
            self.stay_alive_thread.join()
        return 1

    def register(self, user, password):
        register_request = clientServer_pb2.registerRequest(user=user, password=password)
        return self.stub.register(register_request)

    def unregister(self):
        unregister_request = clientServer_pb2.unregisterRequest(user=self.username, password=self.password)
        return self.stub.unregister(unregister_request)

    def put_file(self, filename):
        file_path = f'./data/{filename}'
        
        if not os.path.isfile(file_path):
            print(f'File not found: {file_path}')
            return clientDataNode_pb2.uploadResponse(value=0, response="File not found")

        with open(file_path, 'rb') as f:
            file_data = f.read()

        put_file_request = clientServer_pb2.putFileRequest(username=self.username, filename=filename, size=len(file_data))
        put_file_response = self.stub.putFile(put_file_request)
        
        return self.upload_file(file_data, put_file_response.ip1)

    def upload_file(self, file_data, node_id):
        try:
            with grpc.insecure_channel(f'{node_id}:50052') as channel:
                stubt = clientDataNode_pb2_grpc.ClientDataNodeStub(channel)
                upload_request = clientDataNode_pb2.uploadRequest(username=self.username,
                                                                   filename='filename',
                                                                   data=file_data,
                                                                   node_ip=node_id)
                return stubt.uploadFile(upload_request)
        except grpc.RpcError as e:
            print(f'Error during upload: {e}')
            return clientDataNode_pb2.uploadResponse(value=0, response="Node not found")

    def get_file(self, filename, node_id):
        try:
            with grpc.insecure_channel(f'{node_id}:50052') as channel:
                stubt = clientDataNode_pb2_grpc.ClientDataNodeStub(channel)
                request = clientDataNode_pb2.getRequest(username=self.username, filename=filename)
                response = stubt.getFile(request)

                with open(f'./data/{filename}', 'wb') as f:
                    f.write(response.data)
                return response
        except grpc.RpcError as e:
            print(f'Error during download: {e}')
            return clientDataNode_pb2.getResponse(value=0, response="Node not found")

def main():
    client = Client()
    client.connect()

    while True:
        option = input("Choose an option:\n0. Exit\n1. Log in\n2. Register\n")
        
        if option == '0':
            break
        elif option == "1":
            user = input("Enter your user: ")
            password = input("Enter your password: ")
            response = client.login(user, password)
            print('Logged successfully' if response.value == 1 else response.response)
            
        elif option == "2":
            user = input("Enter your user: ")
            password = input("Enter your password: ")
            response = client.register(user, password)
            print('Registered successfully' if response.value == 1 else response.response)

if __name__ == '__main__':
    main()
        
