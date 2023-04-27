import random
import string

def generate_key(length):
    """Generate a random ASCII key of given length"""
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return key

# Generate a random 128-bit key
key = generate_key(16)
print(key)

# Generate a random 256-bit key
key = generate_key(32)
print(key)

# Generate a random 512-bit key
key = generate_key(64)
print(key)

# Generate a random 1024-bit key
key = generate_key(128)
print(key)

# Generate a random 2048-bit key
key = generate_key(256)
print(key)

# Generate a random 4096-bit key
key = generate_key(512)
print(key)

