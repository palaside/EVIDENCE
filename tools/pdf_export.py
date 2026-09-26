# -*- coding: utf-8 -*-
"""
PDF export service for DIGITAL_EVIDENCE.

The browser owns the exact A4 canvas rendering. This module receives those
canvas snapshots and writes a real multi-page PDF with PyMuPDF.
"""
from __future__ import annotations

import base64
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pymupdf as fitz


DATA_URL_RE = re.compile(r"^data:image/(?P<kind>png|jpeg|jpg);base64,(?P<body>[A-Za-z0-9+/=\r\n]+)$")
SAFE_TITLE_RE = re.compile(r"[^A-Za-z0-9._-]+")
A4_PORTRAIT = fitz.paper_rect("a4")
MAX_PAGES = 500
MAX_PAGE_BYTES = 16 * 1024 * 1024


class PdfExportError(ValueError):
    """Raised when a PDF export request is invalid."""


def _safe_stem(raw_title: str | None) -> str:
    title = (raw_title or "Evidence_Court_Report").strip()
    title = SAFE_TITLE_RE.sub("_", title).strip("._-")
    return title[:80] or "Evidence_Court_Report"


def _decode_image_data_url(value: Any, page_number: int) -> bytes:
    if not isinstance(value, str):
        raise PdfExportError(f"Page {page_number} is not an image data URL.")

    match = DATA_URL_RE.match(value)
    if not match:
        raise PdfExportError(f"Page {page_number} must be a PNG or JPEG data URL.")

    try:
        image_bytes = base64.b64decode(match.group("body"), validate=True)
    except Exception as exc:  # noqa: BLE001 - normalize malformed base64 errors
        raise PdfExportError(f"Page {page_number} contains invalid base64 image data.") from exc

    if not image_bytes:
        raise PdfExportError(f"Page {page_number} is empty.")
    if len(image_bytes) > MAX_PAGE_BYTES:
        raise PdfExportError(f"Page {page_number} exceeds the {MAX_PAGE_BYTES // 1024 // 1024} MB limit.")
    return image_bytes


def export_canvas_pages_to_pdf(payload: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    pages = payload.get("pages")
    if not isinstance(pages, list) or not pages:
        raise PdfExportError("At least one rendered page is required.")
    if len(pages) > MAX_PAGES:
        raise PdfExportError(f"PDF export is limited to {MAX_PAGES} pages per request.")

    title = _safe_stem(payload.get("title"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = base_dir / "Folder_Out"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{title}_{timestamp}.pdf"

    doc = fitz.open()
    try:
        for idx, data_url in enumerate(pages, start=1):
            image_bytes = _decode_image_data_url(data_url, idx)
            page = doc.new_page(width=A4_PORTRAIT.width, height=A4_PORTRAIT.height)
            page.insert_image(page.rect, stream=image_bytes, keep_proportion=False)

        doc.set_metadata(
            {
                "title": title,
                "author": "DIGITAL_EVIDENCE",
                "subject": "Court-ready evidence report generated from verified A4 canvas pages",
                "creator": "DIGITAL_EVIDENCE PyMuPDF PDF Generator",
                "producer": "PyMuPDF",
                "creationDate": datetime.now().strftime("D:%Y%m%d%H%M%S"),
            }
        )
        doc.save(out_path, deflate=True, garbage=4)
    finally:
        doc.close()

    stat = out_path.stat()
    return {
        "status": "ok",
        "file": out_path.name,
        "relativePath": f"Folder_Out/{out_path.name}",
        "url": f"/Folder_Out/{out_path.name}",
        "pages": len(pages),
        "bytes": stat.st_size,
    }
