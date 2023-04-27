import random, os, string
import win32api


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
    """Find a text file in the current directory"""
    root_dirs = findRootDirsWindows()
    for root_dir in root_dirs:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".txt"):
                    print(os.path.join(root, file))


