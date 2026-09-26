"""
Detect Skill - Forensic Image Intake & Classification Gateway
Analyzes image pixels and structure to classify into:
1. TYPE_CHAT -> Routes to Dicut_Chat
2. TYPE_SLIP_SOLO -> Routes to OCR_Slip
3. TYPE_CHAT_WITH_SLIP -> Routes to Search_Slip & Consistent
"""

import os
from enum import Enum, auto
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

class EvidenceType(Enum):
    TYPE_CHAT = auto()
    TYPE_SLIP_SOLO = auto()
    TYPE_CHAT_WITH_SLIP = auto()

@dataclass
class ClassificationResult:
    image_path: str
    type: EvidenceType
    confidence: float
    target_pipeline: str
    details: Dict[str, Any]

def has_green_transfer_badge(img_bgr) -> Tuple[bool, Optional[Tuple[int, int, int, int]]]:
    """Detects presence of bank transfer success badge via HSV color segmentation."""
    if cv2 is None or img_bgr is None:
        return False, None

    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 120, 100])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 150 < area < 10000:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect = float(w) / max(1, h)
            if 0.7 <= aspect <= 1.3:
                return True, (x, y, w, h)
    return False, None

def detect_qr_code(img_bgr) -> bool:
    """Checks for presence of standard QR codes in the image."""
    if cv2 is None or img_bgr is None:
        return False
    try:
        detector = cv2.QRCodeDetector()
        val, points, _ = detector.detectAndDecode(img_bgr)
        return bool(points is not None and len(points) > 0)
    except Exception:
        return False

def classify_evidence_image(image_path: str) -> ClassificationResult:
    """
    Classifies an input evidence image based on pixel features,
    color profiles, and layout structure.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    if cv2 is None:
        # Fallback if OpenCV not loaded
        return ClassificationResult(
            image_path=image_path,
            type=EvidenceType.TYPE_CHAT,
            confidence=0.5,
            target_pipeline="Dicut_Chat",
            details={"fallback": True, "reason": "OpenCV not available"}
        )

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    h, w = img.shape[:2]
    aspect_ratio = float(h) / max(1, w)

    has_badge, badge_box = has_green_transfer_badge(img)
    has_qr = detect_qr_code(img)

    # 1. Standalone Slip Check (Solo)
    # Typically aspect ratio around 1.4 - 2.2, has badge or QR, and card occupies full or nearly full width
    if (has_badge or has_qr) and (1.2 <= aspect_ratio <= 2.5):
        if badge_box:
            bx, by, bw, bh = badge_box
            # If badge is located near top center and badge width is proportionally large (> 4% of img width)
            is_badge_prominent = (bw / float(w)) > 0.04
            is_centered = abs((bx + bw/2.0) - (w / 2.0)) < (w * 0.35)
            
            if is_badge_prominent and is_centered and by < (h * 0.35):
                return ClassificationResult(
                    image_path=image_path,
                    type=EvidenceType.TYPE_SLIP_SOLO,
                    confidence=0.95,
                    target_pipeline="OCR_Slip",
                    details={"aspect_ratio": aspect_ratio, "has_badge": True, "has_qr": has_qr, "prominent": True}
                )

    # 2. Chat with Embedded Slip Check
    # If image has a transfer badge but it's embedded within a sub-bubble or chat background
    if has_badge or has_qr:
        return ClassificationResult(
            image_path=image_path,
            type=EvidenceType.TYPE_CHAT_WITH_SLIP,
            confidence=0.90,
            target_pipeline="Search_Slip & Consistent",
            details={"aspect_ratio": aspect_ratio, "has_badge": has_badge, "has_qr": has_qr, "embedded": True}
        )

    # 3. Pure Chat
    return ClassificationResult(
        image_path=image_path,
        type=EvidenceType.TYPE_CHAT,
        confidence=0.92,
        target_pipeline="Dicut_Chat",
        details={"aspect_ratio": aspect_ratio, "has_badge": False, "has_qr": False}
    )
