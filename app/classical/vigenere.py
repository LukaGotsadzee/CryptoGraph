"""
Vigenère Cipher implementation.

A polyalphabetic substitution cipher that uses a keyword to determine
the shift for each letter. Each letter of the keyword defines a different
shift amount, cycling through the keyword as needed. This is an educational
cipher only — it is NOT cryptographically secure.

Features:
    - Encrypt and decrypt text with a configurable keyword (default: "cryptolab")
    - Preserves original letter case
    - Non-letter characters pass through unchanged and do NOT advance the key index
    - Validates that the keyword is non-empty and contains only letters
"""

# Default keyword specified in the lab requirements
DEFAULT_KEYWORD = "cryptolab"

# Standard English alphabet
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHA_LEN = len(ALPHABET)


def encrypt(text: str, keyword: str = DEFAULT_KEYWORD) -> str:
    """
    Encrypt plaintext using the Vigenère cipher.

    Each letter in the text is shifted forward by the position value of
    the corresponding keyword letter (a=0, b=1, ..., z=25). The keyword
    repeats cyclically. Non-letter characters are preserved unchanged
    and do not consume a keyword letter.

    Args:
        text: The plaintext string to encrypt.
        keyword: The keyword for encryption (default: "cryptolab").
                 Must be non-empty and contain only letters.

    Returns:
        The encrypted ciphertext string.

    Raises:
        ValueError: If the keyword is empty or contains non-letter characters.

    Examples:
        >>> encrypt("Hello Word")
        'Jvnhh Nfkg'
        >>> encrypt("abc", keyword="key")
        'kfa'
    """
    _validate_keyword(keyword)
    return _apply_vigenere(text, keyword.lower(), encrypt_mode=True)


def decrypt(text: str, keyword: str = DEFAULT_KEYWORD) -> str:
    """
    Decrypt ciphertext using the Vigenère cipher.

    Each letter in the text is shifted backward by the position value of
    the corresponding keyword letter. This reverses the encryption process.

    Args:
        text: The ciphertext string to decrypt.
        keyword: The keyword used during encryption (default: "cryptolab").
                 Must be non-empty and contain only letters.

    Returns:
        The decrypted plaintext string.

    Raises:
        ValueError: If the keyword is empty or contains non-letter characters.

    Examples:
        >>> decrypt("Jvnhh Nfkg")
        'Hello Word'
    """
    _validate_keyword(keyword)
    return _apply_vigenere(text, keyword.lower(), encrypt_mode=False)


def _validate_keyword(keyword: str) -> None:
    """
    Validate the Vigenère keyword.

    The keyword must be non-empty and contain only alphabetic characters.

    Args:
        keyword: The keyword to validate.

    Raises:
        ValueError: If the keyword is empty or contains non-letter characters.
    """
    if not keyword:
        raise ValueError("Keyword must not be empty.")
    if not keyword.isalpha():
        raise ValueError(
            f"Keyword must contain only letters, got: '{keyword}'"
        )


def _apply_vigenere(text: str, keyword: str, encrypt_mode: bool) -> str:
    """
    Apply the Vigenère cipher transformation to the text.

    This is the internal engine used by both encrypt() and decrypt().
    In encrypt mode, shifts are added; in decrypt mode, shifts are subtracted.

    Args:
        text: The input string to process.
        keyword: The lowercase keyword to use (already validated).
        encrypt_mode: True for encryption (forward shift),
                      False for decryption (backward shift).

    Returns:
        The transformed text string.
    """
    result = []
    key_len = len(keyword)
    key_index = 0  # Tracks position in the keyword

    for char in text:
        if char.isalpha():
            # Get the shift from the current keyword letter
            shift = ALPHABET.index(keyword[key_index % key_len])

            # Reverse the shift for decryption
            if not encrypt_mode:
                shift = -shift

            # Apply the shift to the character
            char_lower = char.lower()
            char_idx = ALPHABET.index(char_lower)
            new_idx = (char_idx + shift) % ALPHA_LEN
            new_char = ALPHABET[new_idx]

            # Preserve original case
            if char.isupper():
                new_char = new_char.upper()

            result.append(new_char)

            # Advance the key index only for letters
            key_index += 1
        else:
            # Non-letter characters pass through unchanged
            result.append(char)

    return "".join(result)
