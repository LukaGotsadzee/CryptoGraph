"""
Caesar Cipher implementation.

A simple substitution cipher that shifts each letter in the plaintext
by a fixed number of positions in the alphabet. This is an educational
cipher only — it is NOT cryptographically secure.

Features:
    - Encrypt and decrypt text with a configurable shift (default: 3)
    - Support for custom alphabets
    - Preserves original letter case
    - Non-alphabet characters pass through unchanged
"""

# Default English alphabet used when no custom alphabet is provided
DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def encrypt(text: str, shift: int = 3, alphabet: str | None = None) -> str:
    """
    Encrypt plaintext using the Caesar cipher.

    Each letter in the text is shifted forward by the given number of
    positions in the alphabet. Non-alphabet characters are preserved
    unchanged. Letter case is maintained.

    Args:
        text: The plaintext string to encrypt.
        shift: Number of positions to shift each letter (default: 3).
        alphabet: Custom alphabet string (lowercase). If None, uses
                  the standard English alphabet (a-z).

    Returns:
        The encrypted ciphertext string.

    Examples:
        >>> encrypt("Hello Word")
        'Khoor Zrug'
        >>> encrypt("abc", shift=1)
        'bcd'
        >>> encrypt("xyz", shift=3)
        'abc'
    """
    alpha = (alphabet or DEFAULT_ALPHABET).lower()
    return _apply_shift(text, shift, alpha)


def decrypt(text: str, shift: int = 3, alphabet: str | None = None) -> str:
    """
    Decrypt ciphertext using the Caesar cipher.

    Each letter in the text is shifted backward by the given number of
    positions in the alphabet. This reverses the encryption process.

    Args:
        text: The ciphertext string to decrypt.
        shift: Number of positions that were used during encryption (default: 3).
        alphabet: Custom alphabet string (lowercase). Must match the
                  alphabet used during encryption.

    Returns:
        The decrypted plaintext string.

    Examples:
        >>> decrypt("Khoor Zrug")
        'Hello Word'
        >>> decrypt("bcd", shift=1)
        'abc'
    """
    alpha = (alphabet or DEFAULT_ALPHABET).lower()
    return _apply_shift(text, -shift, alpha)


def _apply_shift(text: str, shift: int, alphabet: str) -> str:
    """
    Apply a character shift to the text using the given alphabet.

    This is the internal engine used by both encrypt() and decrypt().
    A positive shift moves letters forward; a negative shift moves
    them backward. The shift wraps around the alphabet length.

    Args:
        text: The input string to process.
        shift: The shift amount (positive for encrypt, negative for decrypt).
        alphabet: The lowercase alphabet to use for shifting.

    Returns:
        The shifted text string.
    """
    result = []
    alpha_len = len(alphabet)

    for char in text:
        lower_char = char.lower()

        # If the character is in our alphabet, shift it
        if lower_char in alphabet:
            idx = alphabet.index(lower_char)
            new_idx = (idx + shift) % alpha_len
            new_char = alphabet[new_idx]

            # Preserve the original case
            if char.isupper():
                new_char = new_char.upper()

            result.append(new_char)
        else:
            # Non-alphabet characters pass through unchanged
            result.append(char)

    return "".join(result)
