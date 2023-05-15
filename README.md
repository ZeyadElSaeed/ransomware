# ransomware
 Project for Computer and Network Security Course, Spring 2023.
 Don't Run Encryption Methods on System Files

 The Following are done:
 ```
 a) Find ALL .txt files in the windows system.
 b) Save these .txt files to a file.
 c) Generate a random 128 bit key (16 characters) using ascii characters.
 d) Use AES (CBC mode) for the encryption process with the random key mentioned at (c).
 e) Save the key used in (c) to desktop in a .key format named "Key.key".
 f) Generate a Public/Private key-pair using RSA in Server Side.
 g) Send the Public Key to the client (Victim)
 h) Encrypt the key in (c) with the Public Key.
 i) Save the encrypted key (h) to a file on the desktop "encryptedKey.key".
 j) Send the encrypted key (h) to the server.
 k) Access the csv file and extract emails from it.
 l) Send the .exe file to the emails in (k).
 ```


 command to install libs for the project:

```
 pip install pypiwin32
 pip install requests
 pip install pycryptodome
 pip install auto-py-to-exe
```
