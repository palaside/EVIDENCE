# Preprocess Service for Slip Reader MVP
"""Service that performs basic image preprocessing steps.
For the MVP we implement stub methods that simply copy the image and
record that preprocessing was performed. In a real system this would
include resizing, deskewing, noise reduction, etc.
"""

import shutil
import os
from datetime import datetime
from typing import Dict

from ..models.slip import PreprocessResult

class PreprocessService:
    """Simple preprocessing implementation.

    Attributes:
        output_dir: Directory where preprocessed images are stored.
    """

    def __init__(self, output_dir: str = "preprocess") -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def preprocess(self, raw_image_path: str) -> PreprocessResult:
        """Copy the raw image to the output directory and return metadata.

        Args:
            raw_image_path: Path to the original uploaded image.
        Returns:
            PreprocessResult containing path to the processed image.
        """
        if not os.path.isfile(raw_image_path):
            raise FileNotFoundError(f"Image not found: {raw_image_path}")
        filename = os.path.basename(raw_image_path)
        dest_path = os.path.join(self.output_dir, filename)
        shutil.copy2(raw_image_path, dest_path)
        details = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": "copy",
        }
        return PreprocessResult(processed_image_path=dest_path, details=details)
