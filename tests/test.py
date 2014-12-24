from speck import spec

import unittest
import shutil
import os
import subprocess


class TestSpeckBinary(unittest.TestCase):
    def test_patch_list(self):
        output = subprocess.check_output(['speck', '--spec', 'tests/test.spec',
                                          'patch', 'list'])
        self.assertEqual(output.decode('utf=8'), "-  ---------\n"
                                                 "0  foo.patch\n"
                                                 "1  bar.patch\n"
                                                 "-  ---------\n")

    def test_source_list(self):
        output = subprocess.check_output(['speck', '--spec', 'tests/test.spec',
                                          'source', 'list'])
        self.assertEqual(output.decode('utf=8'), "-  ----------\n"
                                                 "0  foo.tar.gz\n"
                                                 "0  bar.tar.xz\n"
                                                 "-  ----------\n")

class TestBasicSpec(unittest.TestCase):
    def setUp(self):
        self.parser = spec()
        self.parser.parse("tests/test.spec")

    def test_name(self):
        self.assertEqual(self.parser.name, "test-spec")

    def test_version(self):
        self.assertEqual(self.parser.version, "1.0.0")

    def test_release(self):
        self.assertEqual(self.parser.release, "1%{?dist}")

    def test_summary(self):
        self.assertEqual(self.parser.summary, "test spec for the speck program")

    def test_license(self):
        self.assertEqual(self.parser.license, "BSD")

    def test_URL(self):
        self.assertEqual(self.parser.URL, "foo.bar.com")

    def test_buildarch(self):
        self.assertEqual(self.parser.buildarch, "noarch")

    def test_sources(self):
        self.assertEqual(len(self.parser.sources), 2)
        source = self.parser.sources[0]
        self.assertEqual(source.number, 0)
        self.assertEqual(source.source, "foo.tar.gz")
        self.assertEqual(source.line_no, 12)

    def test_patches(self):
        self.assertEqual(len(self.parser.patches), 2)
        patch = self.parser.patches[0]
        self.assertEqual(patch.number, 0)
        self.assertEqual(patch.source, 'foo.patch')
        self.assertEqual(patch.source_line_no, 15)
        self.assertEqual(patch.applied_line_no, 39)

    def test_globals(self):
        self.assertEqual(len(self.parser.globals), 2)
        g = self.parser.globals[0]
        self.assertEqual(g.name, "pypi_name")
        self.assertEqual(g.value, "click")

    def test_description(self):
        self.assertEqual(self.parser.description.line_no, 31)

    def test_prep(self):
        self.assertEqual(self.parser.prep.line_no, 37)

    def test_build(self):
        self.assertEqual(self.parser.build.line_no, 49)

    def test_install(self):
        self.assertEqual(self.parser.install.line_no, 59)

    def test_check(self):
        self.assertEqual(self.parser.check.line_no, 71)


class TestSpecModifications(unittest.TestCase):
    def setUp(self):
        shutil.copy("tests/test.spec", "tests/modified.spec")
        self.parser = spec()
        self.parser.parse("tests/modified.spec")

    def tearDown(self):
        os.remove("tests/modified.spec")

    def test_patch_add(self):
        self.parser.add_patch("baz.patch")
        added_patch = self.parser.patches[-1]
        self.assertEqual(added_patch.number, 2)
        self.assertEqual(added_patch.source, "baz.patch")
        self.assertEqual(added_patch.source_line_no, 17)
        self.assertEqual(added_patch.applied_line_no, 41)

    def test_patch_remove(self):
        self.parser.remove_patch(0)
        patch = self.parser.patches[0]
        self.assertEqual(patch.number, 1)
        self.assertEqual(patch.source, "bar.patch")
        self.assertEqual(patch.source_line_no, 16)
        self.assertEqual(patch.applied_line_no, 40)


if __name__ == '__main__':
    unittest.main()
