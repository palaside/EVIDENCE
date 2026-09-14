import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from search_slip import search_slips_in_pdf


class TestSearchSlip(unittest.TestCase):
    def setUp(self):
        self.test_pdf = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "Folder_Out",
            "Evidence_Chat_V1.pdf"
        )

    def test_search_slips_on_v1(self):
        if not os.path.exists(self.test_pdf):
            self.skipTest(f"{self.test_pdf} does not exist")

        results = search_slips_in_pdf(self.test_pdf, output_excel=False, output_json=False)
        self.assertGreaterEqual(len(results), 2)
        
        # Check that page 64 is detected
        pages_detected = [p for item in results for p in item["pages"]]
        self.assertIn(64, pages_detected)
        self.assertIn(97, pages_detected)


if __name__ == "__main__":
    unittest.main()
