from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from config.settings import settings
import base64
import json
import os

class EncryptionService:
    """AES-256 encryption service for sensitive data"""
    
    def __init__(self):
        # Ensure key is exactly 32 bytes for AES-256
        self.key = settings.ENCRYPTION_KEY
        if len(self.key) != 32:
            raise ValueError("Encryption key must be exactly 32 bytes for AES-256")
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt string data using AES-256-CBC
        
        Args:
            data: Plain text string to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        try:
            # Generate random IV
            iv = os.urandom(16)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            
            # Pad data to block size
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data.encode()) + padder.finalize()
            
            # Encrypt
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            # Combine IV and encrypted data, then base64 encode
            result = base64.b64encode(iv + encrypted).decode('utf-8')
            return result
            
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt AES-256-CBC encrypted data
        
        Args:
            encrypted_data: Base64 encoded encrypted string
            
        Returns:
            Decrypted plain text string
        """
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # Extract IV and encrypted data
            iv = encrypted_bytes[:16]
            encrypted = encrypted_bytes[16:]
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            # Decrypt
            decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
            
            # Unpad
            unpadder = padding.PKCS7(128).unpadder()
            decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
            
            return decrypted.decode('utf-8')
            
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    def encrypt_dict(self, data: dict) -> str:
        """Encrypt dictionary by converting to JSON first"""
        json_str = json.dumps(data)
        return self.encrypt(json_str)
    
    def decrypt_dict(self, encrypted_data: str) -> dict:
        """Decrypt to dictionary by parsing JSON"""
        json_str = self.decrypt(encrypted_data)
        return json.loads(json_str)

# Singleton instance
encryption_service = EncryptionService()

def encrypt_sensitive_data(data: str) -> str:
    """Helper function to encrypt sensitive data"""
    return encryption_service.encrypt(data)

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Helper function to decrypt sensitive data"""
    return encryption_service.decrypt(encrypted_data)

def encrypt_financial_data(financial_dict: dict) -> str:
    """
    Encrypt financial data dictionary
    
    Args:
        financial_dict: Dictionary containing sensitive financial information
        
    Returns:
        Encrypted string
    """
    return encryption_service.encrypt_dict(financial_dict)

def decrypt_financial_data(encrypted_data: str) -> dict:
    """
    Decrypt financial data
    
    Args:
        encrypted_data: Encrypted string
        
    Returns:
        Dictionary containing financial information
    """
    return encryption_service.decrypt_dict(encrypted_data)
