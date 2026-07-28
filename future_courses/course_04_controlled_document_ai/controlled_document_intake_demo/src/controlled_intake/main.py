from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import __version__
from .errors import CapstoneError
from .fixtures import FixtureAllowlist
from .pipeline import ControlledIntakePipeline
from .providers import build_providers
from .schemas import ApprovalRequest, ApprovalResponse, IntakeResponse
from .settings import Settings
from .usage import build_usage_guard

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOGGER = logging.getLogger("controlled_intake")


def _parse_content_length(values: list[str]) -> int | None:
    if not values:
        return None
    if len(values) != 1:
        raise CapstoneError(
            "INVALID_CONTENT_LENGTH",
            "The Content-Length header must occur exactly once.",
            400,
        )
    value = values[0]
    if (
        not value
        or len(value) > 20
        or not value.isascii()
        or not value.isdecimal()
    ):
        raise CapstoneError(
            "INVALID_CONTENT_LENGTH",
            "The Content-Length header must be a non-negative decimal integer.",
            400,
        )
    return int(value)


async def _read_bounded_body(
    request: Request,
    max_file_bytes: int,
    declared_length: int | None,
) -> bytes:
    chunks: list[bytes] = []
    received = 0
    async for chunk in request.stream():
        received += len(chunk)
        if received > max_file_bytes:
            raise CapstoneError(
                "FILE_TOO_LARGE",
                f"The file exceeds the capstone limit of {max_file_bytes} bytes.",
                413,
            )
        chunks.append(chunk)
    if declared_length is not None and received != declared_length:
        raise CapstoneError(
            "CONTENT_LENGTH_MISMATCH",
            "The received body length did not match Content-Length.",
            400,
        )
    return b"".join(chunks)


def _apply_security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
    )
    return response


def create_app(
    settings: Settings | None = None,
    pipeline: ControlledIntakePipeline | None = None,
) -> FastAPI:
    active_settings = settings or Settings.from_env()
    root = Path(__file__).resolve().parents[2]
    manifest_path = active_settings.fixture_manifest_path
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path

    if pipeline is None:
        document_provider, summary_provider = build_providers(active_settings)
        pipeline = ControlledIntakePipeline(
            active_settings,
            FixtureAllowlist(manifest_path),
            document_provider,
            summary_provider,
            build_usage_guard(active_settings),
        )

    application = FastAPI(
        title="Controlled Document Intake",
        version=__version__,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    application.state.pipeline = pipeline
    application.state.settings = active_settings

    @application.middleware("http")
    async def no_store_and_security_headers(request: Request, call_next):
        try:
            content_length = _parse_content_length(
                request.headers.getlist("content-length")
            )
            if (
                content_length is not None
                and content_length > active_settings.max_file_bytes
            ):
                raise CapstoneError(
                    "REQUEST_TOO_LARGE",
                    "The request exceeds the prototype file limit.",
                    413,
                )
            request.state.declared_content_length = content_length
            response = await call_next(request)
        except CapstoneError as error:
            LOGGER.warning("safe_stop code=%s", error.code)
            response = JSONResponse(
                status_code=error.status_code,
                content={
                    "error": {
                        "code": error.code,
                        "message": error.message,
                    }
                },
            )
        return _apply_security_headers(response)

    @application.exception_handler(CapstoneError)
    async def handle_capstone_error(_request: Request, error: CapstoneError):
        LOGGER.warning("safe_stop code=%s", error.code)
        return JSONResponse(
            status_code=error.status_code,
            content={"error": {"code": error.code, "message": error.message}},
        )

    @application.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _request: Request, _error: RequestValidationError
    ):
        LOGGER.warning("safe_stop code=REQUEST_SCHEMA_REJECTED")
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "REQUEST_SCHEMA_REJECTED",
                    "message": "The request did not match the controlled schema.",
                }
            },
        )

    static_path = root / "static"
    application.mount(
        "/assets", StaticFiles(directory=static_path), name="assets"
    )

    @application.get("/", include_in_schema=False)
    async def index():
        return FileResponse(static_path / "index.html")

    @application.get("/api/health", include_in_schema=False)
    async def health():
        return {
            "status": "ok",
            "version": __version__,
            "provider_mode": active_settings.provider_mode,
            "synthetic_only": True,
            "document_ai_location": "eu",
            "vertex_location": "eu",
            "gemini_model": active_settings.gemini_model,
            "raw_document_storage": False,
        }

    @application.post(
        "/api/intake",
        response_model=IntakeResponse,
        include_in_schema=False,
    )
    async def intake(
        request: Request,
        x_synthetic_acknowledged: str = Header(default=""),
    ):
        if x_synthetic_acknowledged.lower() != "true":
            raise CapstoneError(
                "SYNTHETIC_ACKNOWLEDGEMENT_REQUIRED",
                "Confirm that the selected file is the frozen synthetic course fixture.",
                422,
            )
        content = await _read_bounded_body(
            request,
            active_settings.max_file_bytes,
            request.state.declared_content_length,
        )
        return application.state.pipeline.process(
            content,
            request.headers.get("content-type", "").split(";", 1)[0],
        )

    @application.post(
        "/api/decision",
        response_model=ApprovalResponse,
        include_in_schema=False,
    )
    async def decision(request: ApprovalRequest):
        return application.state.pipeline.decide(request)

    return application


app = create_app()
