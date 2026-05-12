"""
Unit tests for the SHA-256 hashing module.

Tests cover the required lab inputs ("Hello Word" and "LukaGotsadze"),
file hashing, determinism, empty input, and consistency between
text and file hashing of the same content.
"""

import os
import hashlib

import pytest
from app.modern.hashing import hash_text, hash_file


# Pre-computed known SHA-256 digests for verification
HELLO_WORD_HASH = hashlib.sha256(b"Hello Word").hexdigest()
LUKA_GOTSADZE_HASH = hashlib.sha256(b"LukaGotsadze").hexdigest()
EMPTY_STRING_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# Path to the sample test file
SAMPLE_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "sample_data", "LukaGotsadze.txt"
)


# ---------------------------------------------------------------------------
# Required lab test inputs
# ---------------------------------------------------------------------------

class TestHashingRequiredInputs:
    """Tests using the exact strings required by the lab specification."""

    def test_hash_hello_word(self):
        """Hash 'Hello Word' and verify against known digest."""
        result = hash_text("Hello Word")
        assert result == HELLO_WORD_HASH
        assert len(result) == 64  # SHA-256 produces 64 hex chars

    def test_hash_luka_gotsadze(self):
        """Hash 'LukaGotsadze' and verify against known digest."""
        result = hash_text("LukaGotsadze")
        assert result == LUKA_GOTSADZE_HASH

    def test_hash_empty_string(self):
        """Hash of empty string matches the well-known SHA-256 empty digest."""
        result = hash_text("")
        assert result == EMPTY_STRING_HASH


# ---------------------------------------------------------------------------
# File hashing
# ---------------------------------------------------------------------------

class TestFileHashing:
    """Tests for hashing file content."""

    def test_hash_file_bytes(self):
        """Hash raw bytes and verify output format."""
        result = hash_file(b"Hello Word")
        assert result == HELLO_WORD_HASH

    def test_hash_file_matches_text_hash(self):
        """File hash of UTF-8 bytes matches text hash of the same string."""
        text = "LukaGotsadze"
        assert hash_file(text.encode("utf-8")) == hash_text(text)

    def test_hash_sample_file(self):
        """Hash the LukaGotsadze.txt sample file and verify it's valid."""
        with open(SAMPLE_FILE_PATH, "rb") as f:
            file_bytes = f.read()
        result = hash_file(file_bytes)
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_hash_empty_file(self):
        """Hash of empty bytes matches empty string hash."""
        assert hash_file(b"") == EMPTY_STRING_HASH


# ---------------------------------------------------------------------------
# Determinism and properties
# ---------------------------------------------------------------------------

class TestHashingProperties:
    """Tests for SHA-256 properties."""

    def test_deterministic_same_input(self):
        """Same input always produces the same hash."""
        hash1 = hash_text("Hello Word")
        hash2 = hash_text("Hello Word")
        assert hash1 == hash2

    def test_different_inputs_different_hashes(self):
        """Different inputs produce different hashes."""
        hash1 = hash_text("Hello Word")
        hash2 = hash_text("Hello World")
        assert hash1 != hash2

    def test_output_is_lowercase_hex(self):
        """Hash output is a lowercase hexadecimal string."""
        result = hash_text("test")
        assert result == result.lower()
        assert all(c in "0123456789abcdef" for c in result)

    def test_output_length_always_64(self):
        """SHA-256 always produces a 64-character hex string."""
        for text in ["", "a", "Hello Word", "x" * 10000]:
            assert len(hash_text(text)) == 64
