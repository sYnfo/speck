import unittest
from speck import parser

class TestBasicSpec(unittest.TestCase):
    def setUp(self):
        parser.parse("tests/test.spec")

    def test_name(self):
        self.assertEqual(parser.name, "test-spec")

    def test_version(self):
        self.assertEqual(parser.version, "1.0.0")

    def test_release(self):
        self.assertEqual(parser.release, "1%{?dist}")

    def test_summary(self):
        self.assertEqual(parser.summary, "test spec for the speck program")

    def test_patches(self):
        self.assertEqual(str(parser.patches[0]),
                         "Patch number 0, stored in foo.patch, defined at 14 and applied at 38")

if __name__ == '__main__':
    unittest.main()
