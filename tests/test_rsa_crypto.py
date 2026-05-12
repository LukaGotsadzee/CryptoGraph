"""
Unit tests for the RSA encryption/decryption module.

Tests cover key generation, encrypt/decrypt round-trips with required
lab inputs ("Hello Word" and "LukaGotsadze"), wrong-key decryption
failure, plaintext length validation, and key format verification.
"""

import pytest
from app.modern.rsa_crypto import generate_keys, encrypt, decrypt


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------

class TestRSAKeyGeneration:
    """Tests for RSA key pair generation."""

    def test_generates_valid_pem_private_key(self):
        """Generated private key is valid PEM format."""
        private_pem, _ = generate_keys()
        assert private_pem.startswith("-----BEGIN RSA PRIVATE KEY-----")
        assert private_pem.strip().endswith("-----END RSA PRIVATE KEY-----")

    def test_generates_valid_pem_public_key(self):
        """Generated public key is valid PEM format."""
        _, public_pem = generate_keys()
        assert public_pem.startswith("-----BEGIN PUBLIC KEY-----")
        assert public_pem.strip().endswith("-----END PUBLIC KEY-----")

    def test_returns_tuple_of_two_strings(self):
        """generate_keys returns a tuple of two non-empty strings."""
        result = generate_keys()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(k, str) and len(k) > 0 for k in result)

    def test_each_call_generates_unique_keys(self):
        """Each call produces a different key pair."""
        priv1, pub1 = generate_keys()
        priv2, pub2 = generate_keys()
        assert priv1 != priv2
        assert pub1 != pub2

    def test_rejects_key_size_below_minimum(self):
        """Key size below 2048 raises ValueError."""
        with pytest.raises(ValueError, match="at least 2048"):
            generate_keys(key_size=1024)


# ---------------------------------------------------------------------------
# Encrypt/decrypt round-trips
# ---------------------------------------------------------------------------

class TestRSAEncryptDecrypt:
    """Tests for RSA encryption and decryption."""

    @pytest.fixture(autouse=True)
    def _generate_keys(self):
        """Generate a fresh key pair for each test."""
        self.private_pem, self.public_pem = generate_keys()

    def test_roundtrip_hello_word(self):
        """Encrypt and decrypt 'Hello Word' successfully."""
        plaintext = "Hello Word"
        ciphertext = encrypt(plaintext, self.public_pem)
        result = decrypt(ciphertext, self.private_pem)
        assert result == plaintext

    def test_roundtrip_luka_gotsadze(self):
        """Encrypt and decrypt 'LukaGotsadze' successfully."""
        plaintext = "LukaGotsadze"
        ciphertext = encrypt(plaintext, self.public_pem)
        result = decrypt(ciphertext, self.private_pem)
        assert result == plaintext

    def test_ciphertext_is_base64(self):
        """Ciphertext output is a valid base64 string."""
        import base64
        ciphertext = encrypt("test", self.public_pem)
        # Should not raise
        decoded = base64.b64decode(ciphertext)
        assert len(decoded) > 0

    def test_ciphertext_differs_each_time(self):
        """OAEP padding makes each encryption produce different ciphertext."""
        ct1 = encrypt("Hello Word", self.public_pem)
        ct2 = encrypt("Hello Word", self.public_pem)
        # OAEP is randomized, so ciphertexts should differ
        assert ct1 != ct2

    def test_roundtrip_short_text(self):
        """Round-trip works for very short text."""
        plaintext = "a"
        ciphertext = encrypt(plaintext, self.public_pem)
        assert decrypt(ciphertext, self.private_pem) == plaintext


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestRSAErrors:
    """Tests for error conditions."""

    @pytest.fixture(autouse=True)
    def _generate_keys(self):
        """Generate key pairs for error testing."""
        self.private_pem, self.public_pem = generate_keys()
        self.other_private, self.other_public = generate_keys()

    def test_wrong_key_fails_decryption(self):
        """Decrypting with a different private key raises ValueError."""
        ciphertext = encrypt("Hello Word", self.public_pem)
        with pytest.raises(ValueError, match="Decryption failed"):
            decrypt(ciphertext, self.other_private)

    def test_too_long_plaintext_raises_error(self):
        """Plaintext exceeding key capacity raises ValueError."""
        # For 2048-bit key with SHA-256 OAEP: max ~190 bytes
        long_text = "A" * 300
        with pytest.raises(ValueError, match="too long"):
            encrypt(long_text, self.public_pem)

    def test_invalid_public_key_raises_error(self):
        """Invalid PEM string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid public key"):
            encrypt("test", "not-a-valid-pem")

    def test_invalid_private_key_raises_error(self):
        """Invalid PEM string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid private key"):
            decrypt("dGVzdA==", "not-a-valid-pem")

    def test_invalid_base64_ciphertext_raises_error(self):
        """Non-base64 ciphertext raises ValueError."""
        with pytest.raises(ValueError):
            decrypt("!!!not-base64!!!", self.private_pem)
