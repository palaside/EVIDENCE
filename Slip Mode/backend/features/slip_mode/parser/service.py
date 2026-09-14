# Parser service for Slip Reader MVP
"""Service that parses raw OCR text into structured fields.
The implementation uses simple regular expressions to extract common
bank slip attributes such as date, time, amount, reference number and
payer/payee names. This is a lightweight MVP; more sophisticated NLP
can be added later.
"""

import re
from datetime import datetime
from typing import Dict, Any

from ..models.slip import ParseResult

class ParserService:
    """Parse OCR text into structured fields.

    The `parse` method returns a ``ParseResult`` containing the original
    text and a dictionary of extracted fields.
    """

    # Simple regex patterns – adjust as needed for specific slip formats
    DATE_PATTERN = re.compile(r"(?P<date>(?:\d{2}[\/\-]\d{2}[\/\-]\d{4})|(?:\d{4}[\/\-]\d{2}[\/\-]\d{2}))")
    TIME_PATTERN = re.compile(r"(?P<time>\d{2}:\d{2}(?::\d{2})?)")
    AMOUNT_PATTERN = re.compile(r"(?P<amount>\d{1,3}(?:,\d{3})*(?:\.\d{2})?)")
    REFERENCE_PATTERN = re.compile(r"Reference[:\s]+(?P<ref>\w+)", re.IGNORECASE)
    PAYEE_PATTERN = re.compile(r"Payee[:\s]+(?P<payee>.+)", re.IGNORECASE)
    PAYER_PATTERN = re.compile(r"Payer[:\s]+(?P<payer>.+)", re.IGNORECASE)

    def _extract(self, pattern: re.Pattern, text: str) -> Any:
        match = pattern.search(text)
        return match.groupdict().get(next(iter(match.groupdict()))) if match else None

    def parse(self, ocr_text: str) -> ParseResult:
        """Extract fields from the given OCR text.

        Returns a ``ParseResult`` with a ``fields`` dictionary containing
        any values that could be matched.
        """
        fields: Dict[str, Any] = {}
        fields["date"] = self._extract(self.DATE_PATTERN, ocr_text)
        fields["time"] = self._extract(self.TIME_PATTERN, ocr_text)
        amount_str = self._extract(self.AMOUNT_PATTERN, ocr_text)
        if amount_str:
            # Normalise amount to float
            try:
                fields["amount"] = float(amount_str.replace(",", ""))
            except ValueError:
                fields["amount"] = amount_str
        else:
            fields["amount"] = None
        fields["reference"] = self._extract(self.REFERENCE_PATTERN, ocr_text)
        fields["payee"] = self._extract(self.PAYEE_PATTERN, ocr_text)
        fields["payer"] = self._extract(self.PAYER_PATTERN, ocr_text)
        return ParseResult(fields=fields, raw_text=ocr_text)
