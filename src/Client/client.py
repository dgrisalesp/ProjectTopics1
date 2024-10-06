import sys
import os



protos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protos'))
sys.path.append(protos_path)
import clientServer_pb2_grpc, clientServer_pb2
import grpc
import time
import threading



def stayingAlive(timeToLive, id, username):
    def send():   
        while stay:
            stayRequest=clientServer_pb2.stayRequest(id=id, username=username)
            stayResponse= stub.stayingAlive(stayRequest)
            time.sleep(timeToLive)
    thread=threading.Thread(target=send)
    thread.start()
    if not stay:
        thread.join()
        print('Thread finished')
        return
   
        

def login(user, password) :
    login_request=clientServer_pb2.loginRequest(user=user, password=password)
    login_response= stub.login(login_request)
    if login_response.value==1:
        global stay
        stay=True
        stayingAlive(90, login_response.response, user)
    return login_response
def logout():
    global user
    global password
    user=''
    password=''
    global stay
    stay=False
    return 1
def register(user, password):
    register_request=clientServer_pb2.registerRequest(user=user, password=password)
    register_response= stub.register(register_request)
    return register_response
def unregister(user, password):
    unregister_request=clientServer_pb2.unregisterRequest( user=user, password=password)
    unregister_response= stub.unregister(unregister_request)
    return unregister_response
##Important Directions
serverDirection="54.208.98.36"
##

def firstMenu():
    global user
    global password
    while True:
            option=input("Choose an option:\n0. Exit\n1. Log in\n2. Register\n")
            if option=='0':
                return 0
            elif option=="1":
                user=input("Enter your user: ")
                password=input("Enter your password: ")
                respond=login(user, password)
                if respond.value==1:
                    print('Logged successfully')
                    return 1
                elif respond.value==0:
                    print(respond.response)
            elif option=="2":
                user=input("Enter your user: ")
                password=input("Enter your password: ")
                value=register(user, password)
                if value.value==1:
                    return 2
                else:
                    print(value.response)
                    continue


def secondMenu():
    global user
    global password
    while True:
        option=input("Choose an option:\n0. Exit\n1. Log out\n2. Unregister\n3. Put File\n4. Get File\n")
        if option=='0':
            return 0
        elif option=="1":
            logout()
            return 1
        elif option=="2":
            response=unregister(user, password)
            if response.value==1:
                print('Unregistered successfully')
            else:
                print(response.response)
            return 2
        else:
            print('Not a valid option')
if __name__ == '__main__':
    with grpc.insecure_channel(f'{serverDirection}:50051') as channel:
        stub = clientServer_pb2_grpc.ClientServerStub(channel)
        stay=False
        while True:
            first=firstMenu()
            if first==0:
                exit()
            else:
                second=secondMenu()
                if second<=2:
                    continue
                
        # elif option=="3":
        #     stay=False
            
            
        # else:
        #     print('Not a valid option')
            
        
        