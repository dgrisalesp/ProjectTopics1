import sys
import os
from bson import ObjectId
protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)
import clientServer_pb2_grpc, clientServer_pb2
import grpc
import time
from concurrent import futures

#Use log instead of print for velocity
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)


##Mongo connection
from pymongo import MongoClient
from datetime import datetime, timedelta


##Important Directions
mySQLDirection="34.235.171.3"
mongoDirection="3.86.211.136"

class Server(clientServer_pb2_grpc.ClientServerServicer):
    def register(self, request, context):
        ##Obtener el user y el password de la request
        user=request.user
        password=request.password
        try:
            ##Intentar insertar el usuario en la base de datos
            cursor.execute("insert into users values (%s, %s)",(user,password))
            ##Si se logra insertar, se hace commit y se retorna un mensaje de exito
            registerResponse=clientServer_pb2.registerResponse(value=1,response="User registered")
            mydb.commit()
            logging.info(f"User registered {user}")
            return registerResponse
        except Exception as e:
            ##Si no se logra insertar, se hace rollback y se retorna un mensaje de error
            return clientServer_pb2.registerResponse(value=0,response="User not registered")
    def login(self, request, context):
        ##Obtener el user y el password de la request
        user=request.user
        password=request.password
        print(user, password)
        try:
            ##Intentar hacer un select en la base de datos con el user y el password
            cursor.execute("select * from users where user = %s",(user,))
            results=cursor.fetchall()
            if results:
                cursor.execute("select * from users where user = %s and password = %s",(user,password,))
                results=cursor.fetchall()
            
                if results:
                    #print('before insert')
                    id=users.update_one({'username':str(user)}, {'$set':{'seen':datetime.utcnow()}},upsert=True).upserted_id
                    #print(id)
                    if id==None:
                        id=users.find_one({'username':str(user)})['_id']
                    login_response=clientServer_pb2.loginResponse(value=1,response=str(id))
                    return login_response
                else:
                    return clientServer_pb2.loginResponse(value=0,response="Incorrect password")
            else:
                return clientServer_pb2.loginResponse(value=0,response="User does not exist")    
        except:
            return clientServer_pb2.loginResponse(value=0,response="Something went wrong")
    def stayingAlive(self, request, context):
        ##Staying alive se trata de regenerar el seen en mongoDB cada cierto tiempo para que el registro no muera
        user_id=request.id
        username=request.username
        try:
            ##Si todo sale bien se devuelve un value de éxito
            logging.info(f"User {user_id} is alive")
            users.update_one({'_id': ObjectId(user_id), 'username':username }, {'$set':{'seen': datetime.utcnow()}})
            logging.info(f"User {user_id} is still alive")
            return clientServer_pb2.stayResponse(value=1,response="")
        except:
            ##Si algo sale mal, se pide volver a loguearse
            return clientServer_pb2.stayResponse(value=0,response="You have to log in again")
    
    def unregister(self, request, context):
        ##Obtener el user y el password de la request
        user=request.user
        password=request.password
        try:
            ##Intentar eliminar el usuario de la base de datos
            cursor.execute("delete from users where user = %s and password = %s",(user,password))
            
            ##Si se logra eliminar, se hace commit y se retorna un mensaje de exito
            unregisterResponse=clientServer_pb2.unregisterResponse(value=1,response="User unregistered")
            mydb.commit()
            logging.info(f"User unregistered {user}")
            return unregisterResponse
        except:
            ##Si no se logra eliminar, se hace rollback y se retorna un mensaje de error
            return clientServer_pb2.unregisterResponse(value=0,response="User not unregistered")
    def putFile(self, request, context):
        ##Obtener el username, filename y size de la request
        username=request.username
        filename=request.filename
        size=request.size
        try:
            cursor.execute("select ip_address  from nodes  where status=TRUE order by last_used asc limit 1")
            ips=cursor.fetchall()
            response=clientServer_pb2.putFileResponse(value=1, ip1=ips[0][0])
            return response
        except:
            return clientServer_pb2.putFileResponse(value=0, ip1="")
    def receivedFile(self, request, context):
        filename=request.filename
        node_id=request.node_id
        type=request.type
        try:
            cursor.execute("update nodes set last_used=%s where ip_address=%s",(datetime.now(),node_id))
            mydb.commit()
            if type==1:
                cursor.execute("insert into files (node_ip, filename, type) values (%s, %s, %s)",(node_id,filename,type))
                mydb.commit()
                cursor.execute("select ip_address  from nodes  where status=TRUE and ip_address!=%s order by last_used asc limit 1", (node_id, ))
                ips=cursor.fetchall()
                return clientServer_pb2.receivedFileResponse(value=1,id=ips[0][0])
            else:
                cursor.execute("update files set replica=%s where filename=%s",(node_id,filename))
                mydb.commit()
                return clientServer_pb2.receivedFileResponse(value=1,id="")
        except:
            return clientServer_pb2.receivedFileResponse(value=0,id="")

#Define server
def serve():
    ##Se inicia el server y se abre el puerto 50051
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
                client=MongoClient(mongoDirection, 27017)
                db=client['project']
                users=db['users']
                serve()
