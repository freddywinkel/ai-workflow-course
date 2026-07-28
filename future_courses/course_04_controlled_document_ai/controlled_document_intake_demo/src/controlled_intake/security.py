from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from .errors import CapstoneError


def verify_pdf(
    content: bytes,
    content_type: str,
    max_file_bytes: int,
    max_pages: int,
) -> int:
    if content_type != "application/pdf":
        raise CapstoneError(
            "MEDIA_TYPE_REJECTED",
            "Only Portable Document Format (PDF) files are accepted.",
            415,
        )
    if len(content) > max_file_bytes:
        raise CapstoneError(
            "FILE_TOO_LARGE",
            f"The file exceeds the capstone limit of {max_file_bytes} bytes.",
            413,
        )
    if not content.startswith(b"%PDF-"):
        raise CapstoneError(
            "PARSER_CORRUPT_FILE",
            "The allowlisted test file is intentionally corrupt. It stopped "
            "before Document AI, Gemini, or the Firestore usage counter was "
            "called.",
            422,
        )
    try:
        reader = PdfReader(BytesIO(content), strict=True)
        if reader.is_encrypted:
            raise CapstoneError(
                "ENCRYPTED_FILE_REJECTED",
                "Encrypted documents require manual handling in this prototype.",
                422,
            )
        pages = len(reader.pages)
    except CapstoneError:
        raise
    except (PdfReadError, ValueError, OSError) as error:
        raise CapstoneError(
            "PARSER_CORRUPT_FILE",
            f"The document could not be read safely: {type(error).__name__}.",
            422,
        ) from error

    if pages < 1 or pages > max_pages:
        raise CapstoneError(
            "PAGE_LIMIT_REJECTED",
            f"The document has {pages} pages; the capstone limit is {max_pages}.",
            422,
        )
    return pages
