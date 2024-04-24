import socket
import json
from DiffieHellmann import DiffieHellman

class ClientSocket:
    def __init__(self, debug_flag):
        self.__dh = DiffieHellman.DH()
        self.__debug_flag = debug_flag
    
    def initDiffieHellman(self, socket):

        socket.send("connected".encode())

        step1 = socket.recv(1024)

        if self.__debug_flag:
            print(step1)
        

        jsonData = json.loads(step1.decode())
        jsonData = jsonData["dh-keyexchange"]

        self.__dh.base = int(jsonData["base"])
        self.__dh.shared_prime = int(jsonData["prime"])
        publicSecret = int(jsonData["publicSecret"])

        calcedPubSecret = str(self.__dh.calcPublicSecret())
        step2 = {
            "dh-keyexchange": {
                "step": 2,
                "publicSecret": calcedPubSecret
            }
        }

        step2_str = str(step2)
        socket.send(step2_str.encode())

        self.__dh.calc_shared_secret(publicSecret)

    def start_client(self, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, 5000));

            self.initDiffieHellman(sock)
            print("The secret key is {}".format(self.__dh.key))
        finally:
            sock.close()