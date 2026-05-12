"""
RSA Encryption and Decryption implementation.

Provides functions for RSA key pair generation, text encryption
with a public key, and text decryption with a private key.
Uses the `cryptography` library with OAEP padding (SHA-256 + MGF1)
for secure asymmetric encryption.

Security notes:
    - Minimum key size: 2048 bits
    - Padding: OAEP with SHA-256 hash and MGF1
    - RSA can only encrypt data shorter than the key size minus padding overhead
    - Ciphertext is base64-encoded for safe transport in JSON/API responses
    - Keys are serialized in PEM format
"""

import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


# Minimum allowed key size for security
MIN_KEY_SIZE = 2048

# Standard public exponent for RSA
PUBLIC_EXPONENT = 65537


def generate_keys(key_size: int = 2048) -> tuple[str, str]:
    """
    Generate an RSA key pair.

    Creates a new RSA private/public key pair of the specified size
    and returns both keys in PEM format.

    Args:
        key_size: The key size in bits (default: 2048). Must be at
                  least 2048 for security.

    Returns:
        A tuple of (private_key_pem, public_key_pem) as strings.

    Raises:
        ValueError: If key_size is less than 2048.

    Examples:
        >>> private_pem, public_pem = generate_keys()
        >>> private_pem.startswith('-----BEGIN RSA PRIVATE KEY-----')
        True
    """
    if key_size < MIN_KEY_SIZE:
        raise ValueError(
            f"Key size must be at least {MIN_KEY_SIZE} bits, got: {key_size}"
        )

    # Generate the private key
    private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXPONENT,
        key_size=key_size,
    )

    # Serialize private key to PEM
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    # Extract and serialize public key to PEM
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_pem, public_pem


def encrypt(plaintext: str, public_key_pem: str) -> str:
    """
    Encrypt a short text string using an RSA public key.

    The plaintext is encoded to UTF-8, encrypted with OAEP padding,
    and the resulting ciphertext is base64-encoded for safe transport.

    Args:
        plaintext: The text to encrypt. Must be short enough to fit
                   within the RSA key size minus padding overhead
                   (roughly key_size/8 - 66 bytes for SHA-256 OAEP).
        public_key_pem: The RSA public key in PEM format.

    Returns:
        The base64-encoded ciphertext string.

    Raises:
        ValueError: If the plaintext is too long for the key size.
        ValueError: If the public key PEM is invalid.
    """
    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode("utf-8")
        )
    except Exception as e:
        raise ValueError(f"Invalid public key PEM: {e}") from e

    plaintext_bytes = plaintext.encode("utf-8")

    # Check if plaintext fits within key constraints
    # OAEP with SHA-256: max plaintext = key_size_bytes - 2*hash_size - 2
    key_size_bytes = public_key.key_size // 8
    max_plaintext_len = key_size_bytes - 2 * 32 - 2  # SHA-256 hash is 32 bytes
    if len(plaintext_bytes) > max_plaintext_len:
        raise ValueError(
            f"Plaintext too long for RSA key size. "
            f"Max {max_plaintext_len} bytes, got {len(plaintext_bytes)} bytes."
        )

    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return base64.b64encode(ciphertext).decode("utf-8")


def decrypt(ciphertext_b64: str, private_key_pem: str) -> str:
    """
    Decrypt RSA-encrypted ciphertext using a private key.

    The base64-encoded ciphertext is decoded, decrypted with OAEP
    padding, and the resulting plaintext bytes are decoded to a string.

    Args:
        ciphertext_b64: The base64-encoded ciphertext from encrypt().
        private_key_pem: The RSA private key in PEM format.

    Returns:
        The decrypted plaintext string.

    Raises:
        ValueError: If the private key PEM is invalid.
        ValueError: If decryption fails (wrong key or corrupted data).
    """
    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"),
            password=None,
        )
    except Exception as e:
        raise ValueError(f"Invalid private key PEM: {e}") from e

    try:
        ciphertext = base64.b64decode(ciphertext_b64)
    except Exception as e:
        raise ValueError(f"Invalid base64 ciphertext: {e}") from e

    try:
        plaintext_bytes = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}") from e

    return plaintext_bytes.decode("utf-8")
