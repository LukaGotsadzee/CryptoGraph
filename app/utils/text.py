"""
Text processing utilities.

Helper functions for text manipulation used across
the CryptoGraph application.
"""


def sanitize_input(text: str) -> str:
    """
    Sanitize user input text by stripping leading/trailing whitespace.

    Args:
        text: The raw input text.

    Returns:
        The sanitized text string.
    """
    return text.strip()


def is_valid_alphabet(alphabet: str) -> bool:
    """
    Validate a custom alphabet string.

    A valid alphabet must contain only unique lowercase letters
    and have at least 2 characters.

    Args:
        alphabet: The alphabet string to validate.

    Returns:
        True if the alphabet is valid, False otherwise.
    """
    if len(alphabet) < 2:
        return False
    if not alphabet.isalpha() or not alphabet.islower():
        return False
    if len(set(alphabet)) != len(alphabet):
        return False
    return True
