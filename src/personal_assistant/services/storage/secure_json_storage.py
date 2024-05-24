"""
A storage service that encrypts and decrypts data stored in JSON format.
"""
import json
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from personal_assistant.services.storage.base_storage import Storage

class SecureJsonStorage(Storage):
    """
    Storage class that encrypts and decrypts data stored in JSON format.
    """

    def __init__(self):
        load_dotenv()
        self.key = os.getenv('SECRET_KEY')
        self.cipher = Fernet(self.key)

    def save(self, data: dict, path: str) -> None:
        """Encrypt and save data to the specified path."""
        try:
            # Convert the data to JSON and then encrypt it
            json_data = json.dumps(data)
            encrypted_data = self.cipher.encrypt(json_data.encode('utf-8'))
        
            # Write the encrypted data to a file
            with open(path, 'wb') as file:
                file.write(encrypted_data)
        except IOError as e:
            raise IOError(f"Failed to save data to {path}: {e}")

    def load(self, path: str) -> dict:
        """Load and decrypt data from the specified path."""
        try:
            # Read the encrypted data from file
            with open(path, 'rb') as file:
                encrypted_data = file.read()

            # Decrypt the data and convert it from JSON
            decrypted_data = self.cipher.decrypt(encrypted_data)
            json_data = decrypted_data.decode('utf-8')
            return json.loads(json_data)
        except IOError as e:
            raise IOError(f"Failed to load data from {path}: {e}")
