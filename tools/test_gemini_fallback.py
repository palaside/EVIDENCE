#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tools/test_gemini_fallback.py — Unit & Integration Test for Gemini Emergency Fallback
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "_skills", "OCR_Slip", "scripts"))

from gemini_slip_fallback import (
    should_trigger_gemini,
    compute_image_hash,
    recover_unresolved_slip,
    load_api_key,
    load_cache,
    save_cache,
    CACHE_FILE
)


class TestGeminiSlipFallback(unittest.TestCase):

    def test_trigger_logic_complete_slip(self):
        """A complete slip with valid QR and OCR data should NEVER trigger Gemini."""
        complete_slip = {
            "amount": "1,500.00",
            "date": "15/04/2567",
            "time": "14:30",
            "remarks": "0040001234567890",
            "sender_bank": "กสิกรไทย",
            "receiver_bank": "กรุงไทย"
        }
        self.assertFalse(should_trigger_gemini(complete_slip))

    def test_trigger_logic_qr_ok_amount_missing(self):
        """If QR succeeded (remarks is present), do not trigger Gemini because Ref ID is authoritative."""
        slip_with_qr = {
            "amount": "-",
            "date": "15/04/2567",
            "time": "14:30",
            "remarks": "2024041512345678",
            "sender_bank": "ทีเอ็มบีธนชาต (ttb)"
        }
        self.assertFalse(should_trigger_gemini(slip_with_qr))

    def test_trigger_logic_damaged_slip_amount_missing(self):
        """If QR failed AND amount is missing, it MUST trigger Gemini emergency fallback."""
        damaged_slip = {
            "amount": "-",
            "date": "15/04/2567",
            "time": "14:30",
            "remarks": "-",
            "sender_bank": "กรุงไทย"
        }
        self.assertTrue(should_trigger_gemini(damaged_slip))

    def test_trigger_logic_damaged_slip_date_missing(self):
        """If QR failed AND date is missing, it MUST trigger Gemini emergency fallback."""
        damaged_slip = {
            "amount": "500.00",
            "date": "-",
            "time": "-",
            "remarks": "-",
            "sender_bank": "กรุงไทย"
        }
        self.assertTrue(should_trigger_gemini(damaged_slip))

    def test_image_hash_deterministic(self):
        """Hashing must be deterministic SHA-256."""
        dummy_bytes = b"sample_slip_image_data_12345"
        h1 = compute_image_hash(dummy_bytes)
        h2 = compute_image_hash(dummy_bytes)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)

    def test_cache_roundtrip(self):
        """Test persistent cache save and load."""
        test_cache = {"test_hash_123": {"amount": "100.00", "date": "01/01/2567"}}
        save_cache(test_cache)
        loaded = load_cache()
        self.assertIn("test_hash_123", loaded)
        self.assertEqual(loaded["test_hash_123"]["amount"], "100.00")

    def test_recovery_without_api_key_graceful(self):
        """Without API key or with non-triggering slip, recover_unresolved_slip must return original data safely."""
        original = {"amount": "200.00", "date": "10/05/2567", "remarks": "123"}
        result = recover_unresolved_slip(b"dummy", original)
        self.assertEqual(result["amount"], "200.00")
        self.assertEqual(result["date"], "10/05/2567")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeminiSlipFallback)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
