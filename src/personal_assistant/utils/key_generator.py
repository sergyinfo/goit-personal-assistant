from cryptography.fernet import Fernet
key = Fernet.generate_key()

# Save this key securely; you will need it for creating an instance of SecureJsonStorage
print(key.decode())