"""
Pydantic schemas for API request and response models.

Defines all the data models used by the CryptoGraph REST API
for input validation and response serialization.
"""

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Classical cipher schemas
# ---------------------------------------------------------------------------

class CaesarRequest(BaseModel):
    """Request body for Caesar cipher encrypt/decrypt operations."""
    text: str = Field(..., description="The text to encrypt or decrypt")
    shift: int = Field(default=3, description="Number of positions to shift (default: 3)")
    alphabet: str | None = Field(
        default=None,
        description="Custom alphabet string (lowercase). Uses a-z if not provided."
    )


class VigenereRequest(BaseModel):
    """Request body for Vigenère cipher encrypt/decrypt operations."""
    text: str = Field(..., description="The text to encrypt or decrypt")
    keyword: str = Field(
        default="cryptolab",
        description="The keyword for encryption (default: 'cryptolab')"
    )


# ---------------------------------------------------------------------------
# Modern crypto schemas
# ---------------------------------------------------------------------------

class HashRequest(BaseModel):
    """Request body for SHA-256 text hashing."""
    text: str = Field(..., description="The text to hash")


class RSAGenerateRequest(BaseModel):
    """Request body for RSA key pair generation."""
    key_size: int = Field(
        default=2048,
        ge=2048,
        description="RSA key size in bits (minimum: 2048)"
    )


class RSAEncryptRequest(BaseModel):
    """Request body for RSA encryption."""
    text: str = Field(..., description="The plaintext to encrypt")
    public_key: str = Field(..., description="RSA public key in PEM format")


class RSADecryptRequest(BaseModel):
    """Request body for RSA decryption."""
    ciphertext: str = Field(..., description="Base64-encoded ciphertext")
    private_key: str = Field(..., description="RSA private key in PEM format")


class SignTextRequest(BaseModel):
    """Request body for signing text with RSA."""
    text: str = Field(..., description="The text to sign")
    private_key: str = Field(..., description="RSA private key in PEM format")


class VerifyTextRequest(BaseModel):
    """Request body for verifying a text signature."""
    text: str = Field(..., description="The original text that was signed")
    signature: str = Field(..., description="Base64-encoded signature")
    public_key: str = Field(..., description="RSA public key in PEM format")


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class CryptoResponse(BaseModel):
    """Standard response for cryptographic operations."""
    algorithm: str = Field(..., description="Algorithm used (e.g., 'Caesar', 'SHA-256')")
    operation: str = Field(..., description="Operation performed (e.g., 'encrypt', 'hash')")
    input: str = Field(..., description="The original input text")
    result: str = Field(..., description="The result of the operation")


class RSAKeyResponse(BaseModel):
    """Response for RSA key generation."""
    algorithm: str = Field(default="RSA", description="Algorithm name")
    operation: str = Field(default="generate-keys", description="Operation performed")
    key_size: int = Field(..., description="Key size in bits")
    private_key: str = Field(..., description="Private key in PEM format")
    public_key: str = Field(..., description="Public key in PEM format")


class VerifyResponse(BaseModel):
    """Response for signature verification."""
    algorithm: str = Field(default="RSA-PSS", description="Algorithm used")
    operation: str = Field(default="verify", description="Operation performed")
    valid: bool = Field(..., description="Whether the signature is valid")
    message: str = Field(..., description="Human-readable verification result")


class HealthResponse(BaseModel):
    """Response for health check endpoint."""
    status: str = Field(default="ok")
    service: str = Field(default="CryptoGraph API")
