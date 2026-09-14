# OCR package for Slip Reader MVP
"""Defines OCR interface and a simple implementation using pytesseract.
If pytesseract is not available, a fallback stub returns empty text.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional

try:
    import pytesseract
    from PIL import Image
except Exception:  # pragma: no cover
    pytesseract = None
    Image = None

from ..models.slip import OCRResult

class IOCRService(ABC):
    """Abstract OCR service contract."""

    @abstractmethod
    def extract_text(self, image_path: str) -> OCRResult:
        """Extract raw text and confidence from an image.
        Returns an OCRResult.
        """
        pass

class SimpleOCRService(IOCRService):
    """Basic OCR implementation.

    Uses pytesseract when available; otherwise returns empty result.
    """

    def extract_text(self, image_path: str) -> OCRResult:
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        if pytesseract and Image:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            # pytesseract does not provide confidence directly; set dummy
            confidence = 0.9
        else:
            text = ""
            confidence = 0.0
        return OCRResult(text=text, confidence=confidence)
