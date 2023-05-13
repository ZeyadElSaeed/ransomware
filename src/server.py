import socket
from utils import *

# old ip
# SERVER_IP = '172.20.10.2'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678


with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    exported_public_key, exported_private_key = generateRSAKeys()
    key_pair = exported_public_key.decode().replace("\n", "") + "\n" + exported_private_key.decode().replace("\n", "")
    saveKey(key_pair, "keyPair.key")
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn,addr = s.accept()
    print(f'Connection accepted from :{addr}')
    with conn:
        while(True):
            conn.send(exported_public_key)
            data =  conn.recv(1024)
            print(data)
            break


