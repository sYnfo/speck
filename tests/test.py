import unittest
from speck import parser

class TestSpec(unittest.TestCase):
    def test_basic_spec(self):
        parser.parse("tests/test.spec")
        self.assertEqual(parser.name, "test-spec")
        self.assertEqual(parser.version, "1.0.0")
        self.assertEqual(parser.release, "1%{?dist}")
        self.assertEqual(parser.summary, "test spec for the speck program")
        self.assertEqual(str(parser.patches[0]),
                         "Patch number 0, stored in foo.patch, defined at 14 and applied at 38")

if __name__ == '__main__':
    unittest.main()
