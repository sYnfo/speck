from speck import parser
#shitty, I know
parser.parse("tests/test.spec")

import unittest
import shutil
import os

class TestBasicSpec(unittest.TestCase):
    def test_name(self):
        self.assertEqual(parser.name, "test-spec")

    def test_version(self):
        self.assertEqual(parser.version, "1.0.0")

    def test_release(self):
        self.assertEqual(parser.release, "1%{?dist}")

    def test_summary(self):
        self.assertEqual(parser.summary, "test spec for the speck program")

    def test_source(self):
        self.assertEqual(parser.source.number, 0)
        self.assertEqual(parser.source.source, "test_source.tar.gz")
        self.assertEqual(parser.source.line_no, 12)

    def test_patches(self):
        self.assertEqual(str(parser.patches[0]),
                         "Patch number 0, stored in foo.patch, defined at 14 and applied at 38")

    def test_prep(self):
        self.assertEqual(parser.prep.line_no, 36)


class TestSpecModifications(unittest.TestCase):
    def test_patch_add(self):
        parser.add_patch("bar.patch")
        added_patch = parser.patches[-1]
        self.assertEqual(added_patch.patch_number, 2)
        self.assertEqual(added_patch.source, "bar.patch")
        self.assertEqual(added_patch.source_line_no, 16)
        self.assertEqual(added_patch.applied_line_no, 40)


if __name__ == '__main__':
    unittest.main()
