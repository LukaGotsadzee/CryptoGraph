"""
Modern cryptography API routes.

Provides POST endpoints for SHA-256 hashing, RSA key generation,
RSA encryption/decryption, and RSA digital signatures.
"""

from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    HashRequest,
    RSAGenerateRequest,
    RSAEncryptRequest,
    RSADecryptRequest,
    SignTextRequest,
    VerifyTextRequest,
    CryptoResponse,
    RSAKeyResponse,
    VerifyResponse,
)
from app.modern import hashing, rsa_crypto, signatures

router = APIRouter(prefix="/api/modern", tags=["Modern Cryptography"])


# ---------------------------------------------------------------------------
# SHA-256 hashing
# ---------------------------------------------------------------------------

@router.post("/hash/sha256", response_model=CryptoResponse)
async def hash_sha256(request: HashRequest) -> CryptoResponse:
    """Hash text using SHA-256."""
    result = hashing.hash_text(request.text)
    return CryptoResponse(
        algorithm="SHA-256",
        operation="hash",
        input=request.text,
        result=result,
    )


# ---------------------------------------------------------------------------
# RSA key generation
# ---------------------------------------------------------------------------

@router.post("/rsa/generate-keys", response_model=RSAKeyResponse)
async def rsa_generate_keys(
    request: RSAGenerateRequest = RSAGenerateRequest(),
) -> RSAKeyResponse:
    """Generate an RSA key pair."""
    try:
        private_pem, public_pem = rsa_crypto.generate_keys(
            key_size=request.key_size,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RSAKeyResponse(
        key_size=request.key_size,
        private_key=private_pem,
        public_key=public_pem,
    )


# ---------------------------------------------------------------------------
# RSA encryption and decryption
# ---------------------------------------------------------------------------

@router.post("/rsa/encrypt", response_model=CryptoResponse)
async def rsa_encrypt(request: RSAEncryptRequest) -> CryptoResponse:
    """Encrypt text using an RSA public key."""
    try:
        result = rsa_crypto.encrypt(
            plaintext=request.text,
            public_key_pem=request.public_key,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CryptoResponse(
        algorithm="RSA",
        operation="encrypt",
        input=request.text,
        result=result,
    )


@router.post("/rsa/decrypt", response_model=CryptoResponse)
async def rsa_decrypt(request: RSADecryptRequest) -> CryptoResponse:
    """Decrypt RSA ciphertext using a private key."""
    try:
        result = rsa_crypto.decrypt(
            ciphertext_b64=request.ciphertext,
            private_key_pem=request.private_key,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CryptoResponse(
        algorithm="RSA",
        operation="decrypt",
        input=request.ciphertext,
        result=result,
    )


# ---------------------------------------------------------------------------
# RSA digital signatures
# ---------------------------------------------------------------------------

@router.post("/rsa/sign", response_model=CryptoResponse)
async def rsa_sign_text(request: SignTextRequest) -> CryptoResponse:
    """Sign text using an RSA private key."""
    try:
        result = signatures.sign_text(
            text=request.text,
            private_key_pem=request.private_key,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CryptoResponse(
        algorithm="RSA-PSS",
        operation="sign",
        input=request.text,
        result=result,
    )


@router.post("/rsa/verify", response_model=VerifyResponse)
async def rsa_verify_text(request: VerifyTextRequest) -> VerifyResponse:
    """Verify an RSA signature against text."""
    try:
        valid = signatures.verify_text(
            text=request.text,
            signature_b64=request.signature,
            public_key_pem=request.public_key,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return VerifyResponse(
        valid=valid,
        message="Signature is valid" if valid else "Signature is invalid",
    )
