"""
Unit tests for the RSA digital signatures module.

Tests cover sign/verify round-trips for text and file content,
tampered data detection, wrong-key rejection, and the
LukaGotsadze.txt sample file signing workflow.
"""

import os

import pytest
from app.modern.rsa_crypto import generate_keys
from app.modern.signatures import (
    sign_data,
    verify_signature,
    sign_text,
    verify_text,
)


# Path to the sample test file
SAMPLE_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "sample_data", "LukaGotsadze.txt"
)


# ---------------------------------------------------------------------------
# Sign/verify round-trips
# ---------------------------------------------------------------------------

class TestSignatureRoundTrips:
    """Tests for sign → verify round-trips."""

    @pytest.fixture(autouse=True)
    def _generate_keys(self):
        """Generate a fresh key pair for each test."""
        self.private_pem, self.public_pem = generate_keys()

    def test_sign_verify_text_hello_word(self):
        """Sign and verify 'Hello Word' text."""
        signature = sign_text("Hello Word", self.private_pem)
        assert verify_text("Hello Word", signature, self.public_pem)

    def test_sign_verify_text_luka_gotsadze(self):
        """Sign and verify 'LukaGotsadze' text."""
        signature = sign_text("LukaGotsadze", self.private_pem)
        assert verify_text("LukaGotsadze", signature, self.public_pem)

    def test_sign_verify_raw_bytes(self):
        """Sign and verify raw bytes data."""
        data = b"Raw byte content for signing"
        signature = sign_data(data, self.private_pem)
        assert verify_signature(data, signature, self.public_pem)

    def test_sign_verify_file_content(self):
        """Sign and verify the content of LukaGotsadze.txt."""
        with open(SAMPLE_FILE_PATH, "rb") as f:
            file_bytes = f.read()
        signature = sign_data(file_bytes, self.private_pem)
        assert verify_signature(file_bytes, signature, self.public_pem)

    def test_signature_is_base64(self):
        """Signature output is a valid base64 string."""
        import base64
        sig = sign_text("test", self.private_pem)
        decoded = base64.b64decode(sig)
        assert len(decoded) > 0


# ---------------------------------------------------------------------------
# Tamper detection
# ---------------------------------------------------------------------------

class TestSignatureTamperDetection:
    """Tests that tampered data fails verification."""

    @pytest.fixture(autouse=True)
    def _generate_keys(self):
        """Generate a fresh key pair for each test."""
        self.private_pem, self.public_pem = generate_keys()

    def test_tampered_data_fails_verification(self):
        """Modifying the data after signing causes verification to fail."""
        signature = sign_text("Hello Word", self.private_pem)
        # Tamper with the data
        assert not verify_text("Hello World", signature, self.public_pem)

    def test_tampered_signature_fails_verification(self):
        """Modifying the signature causes verification to fail."""
        import base64
        signature = sign_text("Hello Word", self.private_pem)
        # Tamper with the signature by flipping some bytes
        sig_bytes = bytearray(base64.b64decode(signature))
        sig_bytes[0] ^= 0xFF  # Flip first byte
        tampered_sig = base64.b64encode(bytes(sig_bytes)).decode("utf-8")
        assert not verify_text("Hello Word", tampered_sig, self.public_pem)

    def test_wrong_public_key_fails_verification(self):
        """Verifying with a different public key fails."""
        _, other_public = generate_keys()
        signature = sign_text("Hello Word", self.private_pem)
        assert not verify_text("Hello Word", signature, other_public)

    def test_empty_data_sign_verify(self):
        """Signing and verifying empty data works correctly."""
        signature = sign_data(b"", self.private_pem)
        assert verify_signature(b"", signature, self.public_pem)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestSignatureErrors:
    """Tests for error conditions."""

    def test_invalid_private_key_raises_error(self):
        """Invalid private key PEM raises ValueError."""
        with pytest.raises(ValueError, match="Invalid private key"):
            sign_text("test", "not-a-valid-pem")

    def test_invalid_public_key_raises_error(self):
        """Invalid public key PEM raises ValueError."""
        with pytest.raises(ValueError, match="Invalid public key"):
            verify_text("test", "dGVzdA==", "not-a-valid-pem")

    def test_invalid_base64_signature_raises_error(self):
        """Invalid base64 signature raises ValueError."""
        _, public_pem = generate_keys()
        with pytest.raises(ValueError, match="Invalid base64"):
            verify_text("test", "!!!not-base64!!!", public_pem)
