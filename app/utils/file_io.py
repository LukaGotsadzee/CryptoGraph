"""
File I/O utilities.

Helper functions for file handling used in the CryptoGraph
application, primarily for processing uploaded files.
"""


async def read_upload(file) -> bytes:
    """
    Read the contents of an uploaded file.

    Args:
        file: A FastAPI UploadFile object.

    Returns:
        The raw bytes content of the file.
    """
    return await file.read()


def validate_file_size(file_bytes: bytes, max_size_mb: int = 10) -> bool:
    """
    Validate that file content does not exceed the maximum size.

    Args:
        file_bytes: The raw bytes of the file.
        max_size_mb: Maximum allowed file size in megabytes (default: 10).

    Returns:
        True if the file is within the size limit, False otherwise.
    """
    max_bytes = max_size_mb * 1024 * 1024
    return len(file_bytes) <= max_bytes
