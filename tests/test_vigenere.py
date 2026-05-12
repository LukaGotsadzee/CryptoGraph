"""
Unit tests for the Vigenère cipher module.

Tests cover the required lab inputs ("Hello Word" and "LukaGotsadze"),
custom keywords, case preservation, non-letter character handling,
keyword validation, and edge cases.
"""

import pytest
from app.classical.vigenere import encrypt, decrypt


# ---------------------------------------------------------------------------
# Required lab test inputs
# ---------------------------------------------------------------------------

class TestVigenereRequiredInputs:
    """Tests using the exact strings required by the lab specification."""

    def test_encrypt_hello_word_default_key(self):
        """Encrypt 'Hello Word' with default keyword 'cryptolab'."""
        result = encrypt("Hello Word")
        assert result == "Jvjah Kzre"

    def test_decrypt_hello_word_default_key(self):
        """Decrypt back to 'Hello Word' with default keyword 'cryptolab'."""
        result = decrypt("Jvjah Kzre")
        assert result == "Hello Word"

    def test_encrypt_decrypt_hello_word_roundtrip(self):
        """Verify encrypt → decrypt round-trip for 'Hello Word'."""
        plaintext = "Hello Word"
        ciphertext = encrypt(plaintext)
        assert decrypt(ciphertext) == plaintext

    def test_encrypt_luka_gotsadze_default_key(self):
        """Encrypt 'LukaGotsadze' with default keyword 'cryptolab'."""
        result = encrypt("LukaGotsadze")
        assert result == "NlipZcesbfqc"

    def test_decrypt_luka_gotsadze_default_key(self):
        """Decrypt back to 'LukaGotsadze' with default keyword 'cryptolab'."""
        result = decrypt("NlipZcesbfqc")
        assert result == "LukaGotsadze"

    def test_encrypt_decrypt_luka_gotsadze_roundtrip(self):
        """Verify encrypt → decrypt round-trip for 'LukaGotsadze'."""
        plaintext = "LukaGotsadze"
        ciphertext = encrypt(plaintext)
        assert decrypt(ciphertext) == plaintext


# ---------------------------------------------------------------------------
# Custom keyword
# ---------------------------------------------------------------------------

class TestVigenereCustomKeyword:
    """Tests with non-default keywords."""

    def test_encrypt_custom_keyword(self):
        """Encrypt with a custom keyword."""
        result = encrypt("Hello Word", keyword="secret")
        ciphertext = result
        assert decrypt(ciphertext, keyword="secret") == "Hello Word"

    def test_single_char_keyword(self):
        """Single-character keyword behaves like Caesar cipher."""
        # keyword "d" means shift of 3 for every letter (d is index 3)
        result = encrypt("abc", keyword="d")
        assert result == "def"

    def test_keyword_longer_than_text(self):
        """Keyword longer than plaintext uses only needed letters."""
        plaintext = "Hi"
        ciphertext = encrypt(plaintext, keyword="longerkeyword")
        assert decrypt(ciphertext, keyword="longerkeyword") == plaintext

    def test_roundtrip_various_keywords(self):
        """Round-trip verification with several different keywords."""
        keywords = ["key", "abc", "z", "encryption", "XyZ"]
        plaintext = "Hello Word"
        for kw in keywords:
            ciphertext = encrypt(plaintext, keyword=kw)
            assert decrypt(ciphertext, keyword=kw) == plaintext, (
                f"Round-trip failed for keyword: '{kw}'"
            )


# ---------------------------------------------------------------------------
# Case and character preservation
# ---------------------------------------------------------------------------

class TestVigenereCasePreservation:
    """Tests verifying case and non-alpha character handling."""

    def test_preserves_uppercase(self):
        """Uppercase letters remain uppercase after encryption."""
        result = encrypt("ABC", keyword="key")
        for char in result:
            if char.isalpha():
                assert char.isupper()

    def test_preserves_lowercase(self):
        """Lowercase letters remain lowercase after encryption."""
        result = encrypt("abc", keyword="key")
        assert result.islower()

    def test_preserves_mixed_case(self):
        """Mixed case is preserved character by character."""
        plaintext = "HeLLo"
        result = encrypt(plaintext, keyword="abc")
        for orig, enc in zip(plaintext, result):
            if orig.isupper():
                assert enc.isupper()
            else:
                assert enc.islower()

    def test_non_alpha_characters_pass_through(self):
        """Non-letter characters are not encrypted and don't advance the key."""
        plaintext = "A!B@C"
        ciphertext = encrypt(plaintext, keyword="abc")
        decrypted = decrypt(ciphertext, keyword="abc")
        assert decrypted == plaintext

    def test_spaces_preserved_key_not_advanced(self):
        """Spaces pass through and do not consume a keyword letter."""
        # With keyword "ab": a=0, b=1
        # "x y" -> x shifted by 0 = x, space unchanged, y shifted by 1 = z
        result = encrypt("x y", keyword="ab")
        assert result == "x z"


# ---------------------------------------------------------------------------
# Keyword validation
# ---------------------------------------------------------------------------

class TestVigenereValidation:
    """Tests for keyword validation."""

    def test_empty_keyword_raises_error(self):
        """Empty keyword raises ValueError."""
        with pytest.raises(ValueError, match="must not be empty"):
            encrypt("test", keyword="")

    def test_numeric_keyword_raises_error(self):
        """Keyword containing numbers raises ValueError."""
        with pytest.raises(ValueError, match="must contain only letters"):
            encrypt("test", keyword="abc123")

    def test_keyword_with_spaces_raises_error(self):
        """Keyword containing spaces raises ValueError."""
        with pytest.raises(ValueError, match="must contain only letters"):
            encrypt("test", keyword="ab cd")

    def test_keyword_with_special_chars_raises_error(self):
        """Keyword containing special characters raises ValueError."""
        with pytest.raises(ValueError, match="must contain only letters"):
            encrypt("test", keyword="key!")


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestVigenereEdgeCases:
    """Edge case tests."""

    def test_empty_string(self):
        """Encrypting an empty string returns an empty string."""
        assert encrypt("") == ""
        assert decrypt("") == ""

    def test_all_same_letter_keyword(self):
        """Keyword of repeated 'a' (shift 0) returns original text."""
        assert encrypt("Hello Word", keyword="aaa") == "Hello Word"

    def test_only_non_alpha_characters(self):
        """String with no letters returns unchanged."""
        assert encrypt("12345!@#$%") == "12345!@#$%"

    def test_keyword_case_insensitive(self):
        """Keywords are case-insensitive (KEY == key)."""
        upper_result = encrypt("Hello Word", keyword="KEY")
        lower_result = encrypt("Hello Word", keyword="key")
        assert upper_result == lower_result
