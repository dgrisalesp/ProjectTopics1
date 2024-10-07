import sys
import os
from bson import ObjectId
protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)
import clientDataNode_pb2_grpc, clientDataNode_pb2
import grpc
import time
from concurrent import futures

#Use log instead of print for velocity
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)



class FileTransfer(clientDataNode_pb2_grpc.clientDataNodeServicer):
    def uploadFile(self, request, context):
        username=request.username
        filename=request.filename
        try:
            with open(f'./{username}/{filename}','wb' ) as f:
                f.write(request.data)
            return clientDataNode_pb2.uploadResponse(value=1, response="File uploaded succesfully")
        except:
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
        
def serve():
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clientDataNode_pb2_grpc.add_clientDataNodeServicer_to_server(FileTransfer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    serve()