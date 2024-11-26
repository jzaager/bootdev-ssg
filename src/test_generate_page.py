import unittest

from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):

    print("\nTESTING ExtractTitle...")
    print("=================\n")

    def test_extract_title(self):
        md = """# This is my h1

This is random para
"""
        self.assertEqual(extract_title(md), "This is my h1")

        md = """### This is my h3

This is random para

# This is my h1 as last para
"""
        self.assertEqual(extract_title(md), "This is my h1 as last para")

        md = """## This is my h1

This is random para
"""
        self.assertRaises(ValueError, extract_title, md)

