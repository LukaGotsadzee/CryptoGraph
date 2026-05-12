"""
Crypto service layer.

Provides a unified interface for routing cryptographic operations
to the appropriate cipher modules. This service layer abstracts
the module-level functions for use by the API routes.
"""

from app.classical import caesar, vigenere
from app.modern import hashing, rsa_crypto, signatures


class CryptoService:
    """
    Centralized service for all cryptographic operations.

    Routes requests to the appropriate cipher module based on
    the algorithm and operation specified.
    """

    # --- Classical ciphers ---

    @staticmethod
    def caesar_encrypt(text: str, shift: int = 3, alphabet: str | None = None) -> str:
        """Encrypt text using the Caesar cipher."""
        return caesar.encrypt(text, shift=shift, alphabet=alphabet)

    @staticmethod
    def caesar_decrypt(text: str, shift: int = 3, alphabet: str | None = None) -> str:
        """Decrypt text using the Caesar cipher."""
        return caesar.decrypt(text, shift=shift, alphabet=alphabet)

    @staticmethod
    def vigenere_encrypt(text: str, keyword: str = "cryptolab") -> str:
        """Encrypt text using the Vigenère cipher."""
        return vigenere.encrypt(text, keyword=keyword)

    @staticmethod
    def vigenere_decrypt(text: str, keyword: str = "cryptolab") -> str:
        """Decrypt text using the Vigenère cipher."""
        return vigenere.decrypt(text, keyword=keyword)

    # --- Modern crypto ---

    @staticmethod
    def hash_text(text: str) -> str:
        """Hash text using SHA-256."""
        return hashing.hash_text(text)

    @staticmethod
    def hash_file(file_bytes: bytes) -> str:
        """Hash file bytes using SHA-256."""
        return hashing.hash_file(file_bytes)

    @staticmethod
    def rsa_generate_keys(key_size: int = 2048) -> tuple[str, str]:
        """Generate an RSA key pair."""
        return rsa_crypto.generate_keys(key_size=key_size)

    @staticmethod
    def rsa_encrypt(plaintext: str, public_key_pem: str) -> str:
        """Encrypt text with an RSA public key."""
        return rsa_crypto.encrypt(plaintext, public_key_pem)

    @staticmethod
    def rsa_decrypt(ciphertext_b64: str, private_key_pem: str) -> str:
        """Decrypt RSA ciphertext with a private key."""
        return rsa_crypto.decrypt(ciphertext_b64, private_key_pem)

    # --- Signatures ---

    @staticmethod
    def sign_text(text: str, private_key_pem: str) -> str:
        """Sign text with an RSA private key."""
        return signatures.sign_text(text, private_key_pem)

    @staticmethod
    def verify_text(text: str, signature_b64: str, public_key_pem: str) -> bool:
        """Verify an RSA signature against text."""
        return signatures.verify_text(text, signature_b64, public_key_pem)

    @staticmethod
    def sign_data(data: bytes, private_key_pem: str) -> str:
        """Sign raw bytes with an RSA private key."""
        return signatures.sign_data(data, private_key_pem)

    @staticmethod
    def verify_signature(data: bytes, signature_b64: str, public_key_pem: str) -> bool:
        """Verify an RSA signature against raw bytes."""
        return signatures.verify_signature(data, signature_b64, public_key_pem)
