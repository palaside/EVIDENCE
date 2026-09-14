# Upload Service for Slip Reader MVP
"""Service responsible for handling file uploads for bank slips.
It stores the uploaded file in a designated directory and returns metadata.
"""

import os
import uuid
from datetime import datetime
from typing import Tuple

from ..models.slip import UploadResult, Slip

class UploadService:
    """Handles uploading of slip images.

    Attributes:
        storage_dir: Directory where uploaded files are saved.
    """

    def __init__(self, storage_dir: str = "uploads") -> None:
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def upload(self, file_path: str) -> UploadResult:
        """Simulate uploading a file.

        In a real application this would accept a file-like object; for the MVP
        we accept a local file path, copy it into the storage directory, and
        generate a unique identifier.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        slip_id = str(uuid.uuid4())
        _, ext = os.path.splitext(file_path)
        dest_filename = f"{slip_id}{ext}"
        dest_path = os.path.join(self.storage_dir, dest_filename)
        # Copy file
        with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
            dst.write(src.read())

        size_bytes = os.path.getsize(dest_path)
        uploaded_at = datetime.utcnow()
        return UploadResult(
            slip_id=slip_id,
            stored_path=dest_path,
            size_bytes=size_bytes,
            uploaded_at=uploaded_at,
        )

    def create_slip_entity(self, upload_result: UploadResult) -> Slip:
        """Create a Slip domain entity from the upload result."""
        return Slip(
            id=upload_result.slip_id,
            uploaded_at=upload_result.uploaded_at,
            raw_image_path=upload_result.stored_path,
        )
