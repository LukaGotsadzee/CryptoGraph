"""
Classical cipher API routes.

Provides POST endpoints for Caesar and Vigenère cipher
encrypt and decrypt operations.
"""

from fastapi import APIRouter, HTTPException

from app.api.schemas import CaesarRequest, VigenereRequest, CryptoResponse
from app.classical import caesar, vigenere

router = APIRouter(prefix="/api/classical", tags=["Classical Ciphers"])


# ---------------------------------------------------------------------------
# Caesar cipher endpoints
# ---------------------------------------------------------------------------

@router.post("/caesar/encrypt", response_model=CryptoResponse)
async def caesar_encrypt(request: CaesarRequest) -> CryptoResponse:
    """Encrypt text using the Caesar cipher."""
    try:
        result = caesar.encrypt(
            text=request.text,
            shift=request.shift,
            alphabet=request.alphabet,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CryptoResponse(
        algorithm="Caesar",
        operation="encrypt",
        input=request.text,
        result=result,
    )


@router.post("/caesar/decrypt", response_model=CryptoResponse)
async def caesar_decrypt(request: CaesarRequest) -> CryptoResponse:
    """Decrypt text using the Caesar cipher."""
    try:
        result = caesar.decrypt(
            text=request.text,
            shift=request.shift,
            alphabet=request.alphabet,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CryptoResponse(
        algorithm="Caesar",
        operation="decrypt",
        input=request.text,
        result=result,
    )


# ---------------------------------------------------------------------------
# Vigenère cipher endpoints
# ---------------------------------------------------------------------------

@router.post("/vigenere/encrypt", response_model=CryptoResponse)
async def vigenere_encrypt(request: VigenereRequest) -> CryptoResponse:
    """Encrypt text using the Vigenère cipher."""
    try:
        result = vigenere.encrypt(
            text=request.text,
            keyword=request.keyword,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CryptoResponse(
        algorithm="Vigenère",
        operation="encrypt",
        input=request.text,
        result=result,
    )


@router.post("/vigenere/decrypt", response_model=CryptoResponse)
async def vigenere_decrypt(request: VigenereRequest) -> CryptoResponse:
    """Decrypt text using the Vigenère cipher."""
    try:
        result = vigenere.decrypt(
            text=request.text,
            keyword=request.keyword,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CryptoResponse(
        algorithm="Vigenère",
        operation="decrypt",
        input=request.text,
        result=result,
    )
