"""
API integration tests.

Tests the CryptoGraph REST API endpoints using FastAPI's TestClient.
Covers health check, classical cipher endpoints, modern crypto endpoints,
and file upload endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_200(self, client):
        """Health endpoint returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client):
        """Health response contains status 'ok'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "CryptoGraph API"


# ---------------------------------------------------------------------------
# Caesar cipher API
# ---------------------------------------------------------------------------

class TestCaesarAPI:
    """Tests for Caesar cipher endpoints."""

    def test_caesar_encrypt(self, client):
        """Caesar encrypt endpoint returns valid JSON."""
        response = client.post(
            "/api/classical/caesar/encrypt",
            json={"text": "Hello Word"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "Caesar"
        assert data["operation"] == "encrypt"
        assert data["result"] == "Khoor Zrug"

    def test_caesar_decrypt(self, client):
        """Caesar decrypt endpoint returns valid JSON."""
        response = client.post(
            "/api/classical/caesar/decrypt",
            json={"text": "Khoor Zrug"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "Hello Word"

    def test_caesar_custom_shift(self, client):
        """Caesar with custom shift works correctly."""
        response = client.post(
            "/api/classical/caesar/encrypt",
            json={"text": "abc", "shift": 13},
        )
        assert response.status_code == 200
        assert response.json()["result"] == "nop"

    def test_caesar_missing_text_returns_422(self, client):
        """Missing required 'text' field returns 422."""
        response = client.post(
            "/api/classical/caesar/encrypt",
            json={"shift": 3},
        )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# Vigenère cipher API
# ---------------------------------------------------------------------------

class TestVigenereAPI:
    """Tests for Vigenère cipher endpoints."""

    def test_vigenere_encrypt(self, client):
        """Vigenère encrypt endpoint returns valid JSON."""
        response = client.post(
            "/api/classical/vigenere/encrypt",
            json={"text": "Hello Word"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "Vigenère"
        assert data["operation"] == "encrypt"

    def test_vigenere_decrypt_roundtrip(self, client):
        """Vigenère encrypt → decrypt round-trip via API."""
        # Encrypt
        enc_response = client.post(
            "/api/classical/vigenere/encrypt",
            json={"text": "Hello Word", "keyword": "secret"},
        )
        ciphertext = enc_response.json()["result"]

        # Decrypt
        dec_response = client.post(
            "/api/classical/vigenere/decrypt",
            json={"text": ciphertext, "keyword": "secret"},
        )
        assert dec_response.json()["result"] == "Hello Word"

    def test_vigenere_invalid_keyword_returns_400(self, client):
        """Invalid keyword returns 400."""
        response = client.post(
            "/api/classical/vigenere/encrypt",
            json={"text": "test", "keyword": "123"},
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# SHA-256 hashing API
# ---------------------------------------------------------------------------

class TestHashingAPI:
    """Tests for SHA-256 hashing endpoint."""

    def test_hash_text(self, client):
        """SHA-256 hash endpoint returns valid hex digest."""
        response = client.post(
            "/api/modern/hash/sha256",
            json={"text": "Hello Word"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm"] == "SHA-256"
        assert len(data["result"]) == 64


# ---------------------------------------------------------------------------
# RSA API
# ---------------------------------------------------------------------------

class TestRSAAPI:
    """Tests for RSA endpoints."""

    def test_generate_keys(self, client):
        """RSA key generation returns valid PEM keys."""
        response = client.post("/api/modern/rsa/generate-keys")
        assert response.status_code == 200
        data = response.json()
        assert "BEGIN RSA PRIVATE KEY" in data["private_key"]
        assert "BEGIN PUBLIC KEY" in data["public_key"]

    def test_encrypt_decrypt_roundtrip(self, client):
        """RSA encrypt → decrypt round-trip via API."""
        # Generate keys
        keys = client.post("/api/modern/rsa/generate-keys").json()

        # Encrypt
        enc = client.post(
            "/api/modern/rsa/encrypt",
            json={"text": "Hello Word", "public_key": keys["public_key"]},
        )
        assert enc.status_code == 200

        # Decrypt
        dec = client.post(
            "/api/modern/rsa/decrypt",
            json={
                "ciphertext": enc.json()["result"],
                "private_key": keys["private_key"],
            },
        )
        assert dec.status_code == 200
        assert dec.json()["result"] == "Hello Word"

    def test_sign_verify_roundtrip(self, client):
        """RSA sign → verify round-trip via API."""
        keys = client.post("/api/modern/rsa/generate-keys").json()

        # Sign
        sig = client.post(
            "/api/modern/rsa/sign",
            json={"text": "Hello Word", "private_key": keys["private_key"]},
        )
        assert sig.status_code == 200

        # Verify
        ver = client.post(
            "/api/modern/rsa/verify",
            json={
                "text": "Hello Word",
                "signature": sig.json()["result"],
                "public_key": keys["public_key"],
            },
        )
        assert ver.status_code == 200
        assert ver.json()["valid"] is True


# ---------------------------------------------------------------------------
# File upload API
# ---------------------------------------------------------------------------

class TestFileAPI:
    """Tests for file upload endpoints."""

    def test_hash_file(self, client):
        """File hash endpoint handles multipart upload."""
        response = client.post(
            "/api/files/hash",
            files={"file": ("test.txt", b"Hello Word", "text/plain")},
        )
        assert response.status_code == 200
        assert len(response.json()["result"]) == 64

    def test_sign_verify_file_roundtrip(self, client):
        """File sign → verify round-trip."""
        keys = client.post("/api/modern/rsa/generate-keys").json()
        file_content = b"Test file content for signing"

        # Sign file
        sig = client.post(
            "/api/files/sign",
            files={"file": ("doc.txt", file_content, "text/plain")},
            data={"private_key": keys["private_key"]},
        )
        assert sig.status_code == 200

        # Verify file
        ver = client.post(
            "/api/files/verify",
            files={"file": ("doc.txt", file_content, "text/plain")},
            data={
                "signature": sig.json()["result"],
                "public_key": keys["public_key"],
            },
        )
        assert ver.status_code == 200
        assert ver.json()["valid"] is True
