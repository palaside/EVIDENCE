# Models for Slip Reader MVP
"""Data models representing slip entities."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Slip:
    """Domain entity for a bank slip."""
    id: str
    uploaded_at: datetime
    raw_image_path: str
    ocr_text: Optional[str] = None
    parsed_fields: Optional[dict] = None
    validated: bool = False
    export_path: Optional[str] = None

@dataclass
class UploadResult:
    """Result of a file upload operation."""
    slip_id: str
    stored_path: str
    size_bytes: int
    uploaded_at: datetime

@dataclass
class PreprocessResult:
    """Result of image preprocessing."""
    processed_image_path: str
    details: dict

@dataclass
class OCRResult:
    """Result of OCR processing."""
    text: str
    confidence: float

@dataclass
class ParseResult:
    """Structured data extracted from OCR text."""
    fields: dict
    raw_text: str

@dataclass
class ValidationResult:
    """Validation outcome for a parsed slip."""
    is_valid: bool
    errors: List[str]

@dataclass
class ExportResult:
    """Result of exporting slip data to an Excel file."""
    file_path: str
    generated_at: datetime
