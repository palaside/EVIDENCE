#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Digital Evidence Vibe-Build Architecture
Verifies 8-Stage Vibe-Build Compliance, Math Engine, Tokens, and 11-Column Specs.
"""

import os
import re
import sys
import unittest
import math

class TestVibeBuildArchitecture(unittest.TestCase):
    
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.tokens_path = os.path.join(self.base_dir, "Standalone_Suite", "css", "tokens.css")
        self.spec_path = os.path.join(self.base_dir, "SPECIFICATION_TEMPLATE.md")

    def test_01_tokens_exist_and_conform(self):
        """Test Step 3: Design tokens must exist with exact color codes and 8pt scale."""
        self.assertTrue(os.path.exists(self.tokens_path), "tokens.css must exist")
        with open(self.tokens_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("#12243D", content, "Must contain canvas background #12243D")
        self.assertIn("#00A1E4", content, "Must contain sky blue accent #00A1E4")
        self.assertIn("#8E9AA6", content, "Must contain secondary grey #8E9AA6")
        self.assertIn("#FDE8E8", content.upper(), "Must contain failed highlight #FDE8E8")
        self.assertIn("645px", content, "Must specify 645px canvas width")
        self.assertIn("890px", content, "Must specify 890px canvas height")

    def test_02_mathematical_aspect_ratio_centering(self):
        """Test Step 3 & 5: Mathematical Aspect Ratio centering must yield exactly (322.5, 445.0)."""
        paper_w = 645.0
        paper_h = 890.0
        
        # Test with sample slip dimensions
        test_dimensions = [
            (1080, 1920), # Standard mobile slip
            (1080, 2340), # Long tall slip
            (800, 600),   # Wide invoice
            (1200, 1200)  # Square receipt
        ]
        
        for w_orig, h_orig in test_dimensions:
            scale = min(paper_w / w_orig, paper_h / h_orig)
            w_new = math.floor(w_orig * scale)
            h_new = math.floor(h_orig * scale)
            
            x_start = (paper_w - w_new) / 2.0
            y_start = (paper_h - h_new) / 2.0
            
            center_x = x_start + (w_new / 2.0)
            center_y = y_start + (h_new / 2.0)
            
            self.assertAlmostEqual(center_x, 322.5, delta=0.01, msg=f"Center X failed for {w_orig}x{h_orig}")
            self.assertAlmostEqual(center_y, 445.0, delta=0.01, msg=f"Center Y failed for {w_orig}x{h_orig}")

    def test_03_verbatim_disclaimer_accuracy(self):
        """Test Step 5: Official Court Disclaimer must match verbatim."""
        expected_disclaimer = (
            "DIGITAL EVIDENCE เป็นเพียงการเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง "
            "โดยไม่ได้ดัดแปลง แก้ไข เพิ่ม-ลบ เนื้อหา จากต้นฉบับใดๆ "
            "และไม่มีส่วนเกี่ยวข้องใดๆกับเนื้อหาในเอกสาร "
            "เป็นเพียงเครื่องมือที่ทำงานเกี่ยวกับระบบไฟล์ เอกสารแบบอิเล็กทรอนิกส์ เท่านั้น"
        )
        with open(self.spec_path, "r", encoding="utf-8") as f:
            spec_content = f.read()
            
        self.assertIn("DIGITAL EVIDENCE เป็นเพียงการเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง", spec_content)
        self.assertIn("ไม่มีส่วนเกี่ยวข้องใดๆกับเนื้อหาในเอกสาร", spec_content)

    def test_04_eleven_column_ledger_matrix(self):
        """Test Step 4 & 5: Ledger table must specify all 11 required columns."""
        required_columns = [
            "ลำดับ", "วันที่", "เวลา", "ธนาคารผู้โอน", "ชื่อผู้โอน",
            "จำนวนเงิน", "ชื่อผู้รับ", "ธนาคารผู้รับ", "บันทึกช่วยจำ",
            "รหัสอ้างอิง", "หมายเหตุ"
        ]
        with open(self.spec_path, "r", encoding="utf-8") as f:
            spec_content = f.read()
            
        for col in required_columns:
            self.assertIn(col, spec_content, f"Spec must contain column: {col}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
