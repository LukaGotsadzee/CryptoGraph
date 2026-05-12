"""
RSA Digital Signatures implementation.

Provides functions to sign data with an RSA private key and verify
signatures with the corresponding public key. Uses PSS padding with
SHA-256 for secure signature generation and verification.

This module supports signing both text strings and raw file bytes,
making it suitable for document and file integrity verification.

Security notes:
    - Padding: PSS (Probabilistic Signature Scheme) with SHA-256
    - Salt length: Maximum available (PSS.MAX_LENGTH)
    - Signatures are base64-encoded for safe transport
"""

import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, utils


def sign_data(data: bytes, private_key_pem: str) -> str:
    """
    Sign raw bytes with an RSA private key.

    Creates a digital signature using PSS padding with SHA-256.
    The signature is base64-encoded for safe transport in JSON/API.

    Args:
        data: The raw bytes to sign (text encoded to bytes, or file content).
        private_key_pem: The RSA private key in PEM format.

    Returns:
        The base64-encoded signature string.

    Raises:
        ValueError: If the private key PEM is invalid.

    Examples:
        >>> from app.modern.rsa_crypto import generate_keys
        >>> priv, pub = generate_keys()
        >>> sig = sign_data(b"Hello Word", priv)
        >>> verify_signature(b"Hello Word", sig, pub)
        True
    """
    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"),
            password=None,
        )
    except Exception as e:
        raise ValueError(f"Invalid private key PEM: {e}") from e

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    return base64.b64encode(signature).decode("utf-8")


def verify_signature(
    data: bytes, signature_b64: str, public_key_pem: str
) -> bool:
    """
    Verify an RSA digital signature against data.

    Checks whether the provided signature is valid for the given data
    using the corresponding RSA public key.

    Args:
        data: The raw bytes that were originally signed.
        signature_b64: The base64-encoded signature to verify.
        public_key_pem: The RSA public key in PEM format.

    Returns:
        True if the signature is valid, False otherwise.

    Raises:
        ValueError: If the public key PEM or signature encoding is invalid.
    """
    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode("utf-8")
        )
    except Exception as e:
        raise ValueError(f"Invalid public key PEM: {e}") from e

    try:
        signature = base64.b64decode(signature_b64)
    except Exception as e:
        raise ValueError(f"Invalid base64 signature: {e}") from e

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


def sign_text(text: str, private_key_pem: str) -> str:
    """
    Sign a text string with an RSA private key.

    Convenience wrapper that encodes the text to UTF-8 bytes
    before signing.

    Args:
        text: The text string to sign.
        private_key_pem: The RSA private key in PEM format.

    Returns:
        The base64-encoded signature string.
    """
    return sign_data(text.encode("utf-8"), private_key_pem)


def verify_text(text: str, signature_b64: str, public_key_pem: str) -> bool:
    """
    Verify a signature against a text string.

    Convenience wrapper that encodes the text to UTF-8 bytes
    before verification.

    Args:
        text: The original text string that was signed.
        signature_b64: The base64-encoded signature.
        public_key_pem: The RSA public key in PEM format.

    Returns:
        True if the signature is valid, False otherwise.
    """
    return verify_signature(text.encode("utf-8"), signature_b64, public_key_pem)
