import sys
import os
protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)
import clientServer_pb2_grpc, clientServer_pb2
import grpc
import time
from concurrent import futures

#Use log instead of print for velocity
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)


mySQLDirection="98.82.35.86"
class Server(clientServer_pb2_grpc.ClientServerServicer):
    def register(self, request, context):
        user=request.user
        password=request.password
        logging.info(user, password)
        try:
            cursor.execute("insert into users values (%s, %s)",(user,password))
            registerResponse=clientServer_pb2.registerResponse(response="User registered")
            mydb.commit()
            logging.info(f"User registered {user}")
            return registerResponse
        except Exception as e:
            logging.info(e)
            return clientServer_pb2.registerResponse(response="User not registered")

#Define server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clientServer_pb2_grpc.add_ClientServerServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    ##Connect database running on mysql server
    import mysql.connector
    with mysql.connector.connect(
        host=mySQLDirection,
        user="dgrisalesp",
        password="password",
        database="project"
    ) as mydb:
            with mydb.cursor() as cursor:
                #Call the serve function
                serve()
