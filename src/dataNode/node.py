import sys
import os
from bson import ObjectId
protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)
import clientDataNode_pb2_grpc, clientDataNode_pb2, clientServer_pb2_grpc, clientServer_pb2
import grpc
import time
from concurrent import futures

#Use log instead of print for velocity
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)





serverDirection="54.198.253.100"
def receivedFile(filename, node_id, type):
    try:
        with grpc.insecure_channel(f'{serverDirection}:50051') as channel:
            stub = clientServer_pb2_grpc.ClientServerStub(channel)
            receivedFileRequest=clientServer_pb2.receivedFileRequest(filename=filename, node_id=node_id, type=type)
            receivedFileResponse=stub.receivedFile(receivedFileRequest)
            return receivedFileResponse
    except:
        return clientServer_pb2.receivedFileResponse(value=0, id="")


class FileTransfer(clientDataNode_pb2_grpc.ClientDataNodeServicer):
    
    def uploadFile(self, request, context):
        print("llegó")
        username=request.username
        filename=request.filename
        home_directory = os.path.expanduser('~')
        directory = os.path.join(home_directory, username)
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            with open(f'{directory}/{filename}','wb' ) as f:
                print('Abrió')
                f.write(request.data)
                filename=f'{directory}/{filename}'
                print("Good")
                response=receivedFile(filename, request.node_id, 1)
                sendReplicaRequest=clientDataNode_pb2.sendReplicaRequest(filename=filename, node_id=response.id, data=request.data)
                with grpc.insecure_channel(f'{response.node_id}:50052') as channel:
                    stub=clientDataNode_pb2_grpc.ClientDataNodeStub(channel)
                    sendReplicaResponse=stub.sendReplica(sendReplicaRequest)
                    if sendReplicaResponse.value==1:
                        return clientDataNode_pb2.uploadResponse(value=1, response="File uploaded succesfully")
                    else:
                        return clientDataNode_pb2.uploadResponse(value=0, response="File not uploaded")
        except:
            print('Falló')
            return clientDataNode_pb2.uploadResponse(value=0, response="File not uploaded") 
        
    def getFile(self, request, context):
        username=request.username
        filename=request.filename
        try:
            with open(f'./{username}/{filename}','rb') as f:
                data=f.read()
            return clientDataNode_pb2.getResponse(value=1, response="File downloaded succesfully", data=data)
        except:
            return clientDataNode_pb2.getResponse(value=0, response="File not downloaded")
    
    def sendReplica(self, request, context):
        filename=request.filename
        node_id=request.node_id
        try:
            with open(filename, 'wb') as f:
                f.write(request.data)
                receivedFile(filename, node_id, 2)
            return clientDataNode_pb2.sendReplica(value=1, response="File uploaded succesfully")
        except:
            return clientDataNode_pb2.sendReplica(value=0, response="Something went wrong")
            
            
def serve():
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clientDataNode_pb2_grpc.add_ClientDataNodeServicer_to_server(FileTransfer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    serve()