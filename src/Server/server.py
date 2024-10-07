import sys
import os
import logging
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
import grpc
from concurrent import futures
import mysql.connector

# Set up logging
logging.basicConfig(format='%(message)s', level=logging.INFO)

# Set up paths for protobuf files
protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)

# Import generated gRPC classes
import clientServer_pb2_grpc, clientServer_pb2

# Database connection details
MYSQL_HOST = "34.235.171.3"
MONGO_HOST = "3.86.211.136"

class Server(clientServer_pb2_grpc.ClientServerServicer):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register(self, request, context):
        user, password = request.user, request.password
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, password))
            self.db_connection.commit()
            logging.info(f"User registered: {user}")
            return clientServer_pb2.registerResponse(value=1, response="User registered")
        except Exception as e:
            logging.error(f"Registration failed for {user}: {e}")
            self.db_connection.rollback()
            return clientServer_pb2.registerResponse(value=0, response="User not registered")

    def login(self, request, context):
        user, password = request.user, request.password
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (user,))
            if cursor.fetchone():
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, password))
                if cursor.fetchone():
                    user_id = self.update_user_seen(user)
                    return clientServer_pb2.loginResponse(value=1, response=str(user_id))
                else:
                    return clientServer_pb2.loginResponse(value=0, response="Incorrect password")
            else:
                return clientServer_pb2.loginResponse(value=0, response="User does not exist")
        except Exception as e:
            logging.error(f"Login failed for {user}: {e}")
            return clientServer_pb2.loginResponse(value=0, response="Something went wrong")

    def update_user_seen(self, username):
        user_id = users.update_one({'username': username}, {'$set': {'seen': datetime.utcnow()}}, upsert=True).upserted_id
        if user_id is None:
            user_id = users.find_one({'username': username})['_id']
        return user_id

    def stayingAlive(self, request, context):
        user_id = request.id
        username = request.username
        try:
            logging.info(f"User {user_id} is alive")
            users.update_one({'_id': ObjectId(user_id), 'username': username}, {'$set': {'seen': datetime.utcnow()}})
            return clientServer_pb2.stayResponse(value=1, response="")
        except Exception as e:
            logging.error(f"Staying alive failed for {user_id}: {e}")
            return clientServer_pb2.stayResponse(value=0, response="You have to log in again")

    def unregister(self, request, context):
        user, password = request.user, request.password
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM users WHERE username = %s AND password = %s", (user, password))
            self.db_connection.commit()
            logging.info(f"User unregistered: {user}")
            return clientServer_pb2.unregisterResponse(value=1, response="User unregistered")
        except Exception as e:
            logging.error(f"Unregistration failed for {user}: {e}")
            self.db_connection.rollback()
            return clientServer_pb2.unregisterResponse(value=0, response="User not unregistered")

    def putFile(self, request, context):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT ip_address FROM nodes WHERE status=TRUE ORDER BY last_used ASC LIMIT 1")
            ips = cursor.fetchall()
            
            if ips:
                return clientServer_pb2.putFileResponse(value=1, ip1=ips[0][0])
            else:
                return clientServer_pb2.putFileResponse(value=0, ip1="")
        except Exception as e:
            logging.error(f"Error in putFile: {e}")
            return clientServer_pb2.putFileResponse(value=0, ip1="")

    def receivedFile(self, request, context):
        filename = request.filename
        node_id = request.node_id
        file_type = request.type
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("UPDATE nodes SET last_used=%s WHERE ip_address=%s", (datetime.now(), node_id))
            
            if file_type == 1:
                cursor.execute("INSERT INTO files (node_ip, filename, type) VALUES (%s, %s, %s)", (node_id, filename, file_type))
                self.db_connection.commit()

                cursor.execute("SELECT ip_address FROM nodes WHERE status=TRUE AND ip_address!=%s ORDER BY last_used ASC LIMIT 1", (node_id,))
                ips = cursor.fetchall()
                
                return clientServer_pb2.receivedFileResponse(value=1, id=ips[0][0] if ips else "")
                
            else:
                cursor.execute("UPDATE files SET replica=%s WHERE filename=%s", (node_id, filename))
                self.db_connection.commit()
                return clientServer_pb2.receivedFileResponse(value=1, id="")
                
        except Exception as e:
            logging.error(f"Error in receivedFile for {filename}: {e}")
            return clientServer_pb2.receivedFileResponse(value=0, id="")

def serve(db_connection):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clientServer_pb2_grpc.add_ClientServerServicer_to_server(Server(db_connection), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    with mysql.connector.connect(
        host=MYSQL_HOST,
        user="dgrisalesp",
        password="password",
        database="project"
    ) as mydb:
        
        # Connect to MongoDB
        mongo_client = MongoClient(MONGO_HOST)
        db = mongo_client['project']
        users = db['users']
        
        # Start the gRPC server
        serve(mydb)
