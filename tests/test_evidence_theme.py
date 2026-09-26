import unittest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

class TestEvidenceTheme(unittest.TestCase):
    def test_theme_imports_and_renders(self):
        from core.evidence_theme import (
            load_evidence_fonts,
            load_evidence_logo,
            apply_header_ribbon,
            apply_footer_disclaimer,
            create_evidence_canvas
        )
        fonts = load_evidence_fonts()
        self.assertIn("header_lbl", fonts)
        self.assertIn("header_val", fonts)
        self.assertIn("footer", fonts)

        canvas = create_evidence_canvas(993, 1406)
        logo = load_evidence_logo(75)
        apply_header_ribbon(canvas, mode="TARGET EVIDENCE", corroborated="บุคคลเป้าหมาย: จิณห์นิภา", page_str="1 / 10", fonts=fonts, logo_img=logo)
        apply_footer_disclaimer(canvas, fonts=fonts)
        self.assertEqual(canvas.size, (993, 1406))

    def test_fit_slip_block_full_fill(self):
        from core.evidence_theme import fit_slip_block
        # Create a small slip image (400x600)
        small_slip = Image.new("RGB", (400, 600), (240, 240, 240))
        block = fit_slip_block(small_slip, target_w=645, target_h=890)
        self.assertEqual(block.size, (645, 890))

if __name__ == "__main__":
    unittest.main()
