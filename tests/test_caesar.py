"""
Unit tests for the Caesar cipher module.

Tests cover the required lab inputs ("Hello Word" and "LukaGotsadze"),
custom shift values, case preservation, non-alphabet character handling,
custom alphabet support, and edge cases.
"""

import pytest
from app.classical.caesar import encrypt, decrypt


# ---------------------------------------------------------------------------
# Required lab test inputs
# ---------------------------------------------------------------------------

class TestCaesarRequiredInputs:
    """Tests using the exact strings required by the lab specification."""

    def test_encrypt_hello_word_default_shift(self):
        """Encrypt 'Hello Word' with default shift of 3."""
        result = encrypt("Hello Word")
        assert result == "Khoor Zrug"

    def test_decrypt_hello_word_default_shift(self):
        """Decrypt back to 'Hello Word' with default shift of 3."""
        result = decrypt("Khoor Zrug")
        assert result == "Hello Word"

    def test_encrypt_decrypt_hello_word_roundtrip(self):
        """Verify encrypt → decrypt round-trip for 'Hello Word'."""
        plaintext = "Hello Word"
        ciphertext = encrypt(plaintext)
        assert decrypt(ciphertext) == plaintext

    def test_encrypt_luka_gotsadze_default_shift(self):
        """Encrypt 'LukaGotsadze' with default shift of 3."""
        result = encrypt("LukaGotsadze")
        assert result == "OxndJrwvdgch"

    def test_decrypt_luka_gotsadze_default_shift(self):
        """Decrypt back to 'LukaGotsadze' with default shift of 3."""
        result = decrypt("OxndJrwvdgch")
        assert result == "LukaGotsadze"

    def test_encrypt_decrypt_luka_gotsadze_roundtrip(self):
        """Verify encrypt → decrypt round-trip for 'LukaGotsadze'."""
        plaintext = "LukaGotsadze"
        ciphertext = encrypt(plaintext)
        assert decrypt(ciphertext) == plaintext


# ---------------------------------------------------------------------------
# Custom shift values
# ---------------------------------------------------------------------------

class TestCaesarCustomShift:
    """Tests with non-default shift values."""

    def test_encrypt_shift_1(self):
        """Encrypt with shift of 1."""
        assert encrypt("abc", shift=1) == "bcd"

    def test_decrypt_shift_1(self):
        """Decrypt with shift of 1."""
        assert decrypt("bcd", shift=1) == "abc"

    def test_encrypt_shift_13_rot13(self):
        """Encrypt with shift of 13 (ROT13)."""
        assert encrypt("Hello Word", shift=13) == "Uryyb Jbeq"

    def test_decrypt_shift_13_rot13(self):
        """Decrypt ROT13 ciphertext."""
        assert decrypt("Uryyb Jbeq", shift=13) == "Hello Word"

    def test_roundtrip_shift_25(self):
        """Verify round-trip with large shift value (25)."""
        plaintext = "LukaGotsadze"
        ciphertext = encrypt(plaintext, shift=25)
        assert decrypt(ciphertext, shift=25) == plaintext


# ---------------------------------------------------------------------------
# Case and character preservation
# ---------------------------------------------------------------------------

class TestCaesarCasePreservation:
    """Tests verifying case and non-alpha character handling."""

    def test_preserves_uppercase(self):
        """Uppercase letters remain uppercase after encryption."""
        result = encrypt("ABC")
        assert result == "DEF"
        assert result.isupper()

    def test_preserves_lowercase(self):
        """Lowercase letters remain lowercase after encryption."""
        result = encrypt("abc")
        assert result == "def"
        assert result.islower()

    def test_preserves_mixed_case(self):
        """Mixed case is preserved character by character."""
        result = encrypt("AbCdEf")
        assert result == "DeFgHi"

    def test_preserves_spaces(self):
        """Spaces pass through unchanged."""
        result = encrypt("a b c")
        assert result == "d e f"

    def test_preserves_punctuation(self):
        """Punctuation marks pass through unchanged."""
        result = encrypt("Hello, World!")
        assert result == "Khoor, Zruog!"

    def test_preserves_numbers(self):
        """Digits pass through unchanged."""
        result = encrypt("abc123def")
        assert result == "def123ghi"


# ---------------------------------------------------------------------------
# Custom alphabet
# ---------------------------------------------------------------------------

class TestCaesarCustomAlphabet:
    """Tests with a custom alphabet."""

    def test_encrypt_custom_alphabet(self):
        """Encrypt using a short custom alphabet."""
        custom = "abcd"
        assert encrypt("abcd", shift=1, alphabet=custom) == "bcda"

    def test_decrypt_custom_alphabet(self):
        """Decrypt using a short custom alphabet."""
        custom = "abcd"
        assert decrypt("bcda", shift=1, alphabet=custom) == "abcd"

    def test_roundtrip_custom_alphabet(self):
        """Verify round-trip with custom alphabet."""
        custom = "zyxwvutsrqponmlkjihgfedcba"  # reversed alphabet
        plaintext = "hello"
        ciphertext = encrypt(plaintext, shift=3, alphabet=custom)
        assert decrypt(ciphertext, shift=3, alphabet=custom) == plaintext

    def test_characters_not_in_custom_alphabet_pass_through(self):
        """Characters not in the custom alphabet are preserved."""
        custom = "abc"
        # 'd' is not in the custom alphabet, so it passes through
        assert encrypt("abcd", shift=1, alphabet=custom) == "bcad"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestCaesarEdgeCases:
    """Edge case tests."""

    def test_empty_string(self):
        """Encrypting an empty string returns an empty string."""
        assert encrypt("") == ""
        assert decrypt("") == ""

    def test_shift_zero(self):
        """Shift of 0 returns the original text unchanged."""
        assert encrypt("Hello Word", shift=0) == "Hello Word"

    def test_shift_26_full_rotation(self):
        """Shift of 26 (full rotation) returns the original text."""
        assert encrypt("Hello Word", shift=26) == "Hello Word"

    def test_negative_shift(self):
        """Negative shift works correctly (shifts backward)."""
        assert encrypt("def", shift=-3) == "abc"

    def test_shift_larger_than_alphabet(self):
        """Shift larger than alphabet length wraps correctly."""
        assert encrypt("abc", shift=29) == "def"  # 29 % 26 == 3
