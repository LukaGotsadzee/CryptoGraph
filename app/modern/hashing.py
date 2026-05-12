"""
SHA-256 Hashing implementation.

Provides functions to compute SHA-256 cryptographic hash digests
for both text strings and raw file bytes. Uses Python's built-in
hashlib module which wraps OpenSSL's SHA-256 implementation.

SHA-256 is a one-way hash function — it is computationally infeasible
to reverse the hash back to the original input.
"""

import hashlib


def hash_text(text: str) -> str:
    """
    Compute the SHA-256 hash of a text string.

    The text is encoded to UTF-8 bytes before hashing.

    Args:
        text: The input string to hash.

    Returns:
        The hexadecimal SHA-256 digest string (64 characters).

    Examples:
        >>> hash_text("Hello Word")
        'a]...64-char hex string...'
        >>> hash_text("")
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_file(file_bytes: bytes) -> str:
    """
    Compute the SHA-256 hash of raw file content.

    Accepts file content as bytes and returns the hex digest.
    For large files, this processes the entire content in memory.

    Args:
        file_bytes: The raw bytes of the file to hash.

    Returns:
        The hexadecimal SHA-256 digest string (64 characters).

    Examples:
        >>> hash_file(b"Hello Word")
        'a]...same as hash_text("Hello Word")...'
    """
    return hashlib.sha256(file_bytes).hexdigest()
