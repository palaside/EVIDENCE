#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
_engines/Typhoon_OCR/scripts/typhoon_ocr.py — OpenTyphoon Thai Document & Slip OCR Specialist (Mirror)
"""

import os
import sys

# Import directly from _skills
ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, "..", "..", ".."))
SKILL_SCRIPT = os.path.join(PROJECT_ROOT, "_skills", "Typhoon_OCR", "scripts")

if os.path.exists(SKILL_SCRIPT) and SKILL_SCRIPT not in sys.path:
    sys.path.insert(0, SKILL_SCRIPT)

from typhoon_ocr import (
    load_api_key,
    ocr_image_raw,
    judge_structured_slip,
    process_slip,
    main
)

if __name__ == "__main__":
    main()
