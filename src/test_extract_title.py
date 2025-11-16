import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Starting with a title\n\n## Subtitle right here\n\n"
        res = extract_title(md)
        self.assertEqual(res, "Starting with a title")
