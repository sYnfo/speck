import re

from entities import LineParser, Patch

class spec():
    def __init__(self):
        self.parsers = []
        self.patches = []

    def parse(self, spec_file):
        self.spec_file = spec_file
        with open(spec_file, 'r') as f:
            for self.line_no, line in enumerate(f, start=1):
                for p in self.parsers:
                    match = re.match(p.regexp, line)
                    if match:
                        p.consume(self, *match.groups())

    # do not implement this in the parser, should be in a plugin
    def add_patch(self, patch_file):
        last_patch = sorted(self.patches, key=lambda x: x.source_line_no)[-1]

        with open(self.spec_file, 'rw') as s:
            lines = s.readlines()
            lines.insert(last_patch.source_line_no + 1,
                         "Patch{}: {}\n".format(last_patch.patch_number + 1,
                                                patch_file))
            lines.insert(last_patch.applied_line_no + 1,
                         "%patch{} -p1\n".format(last_patch.patch_number + 1))

        with open(self.spec_file, 'w') as s:
            s.writelines(lines)

        new_patch = Patch(patch_number=last_patch.patch_number + 1,
                          source=patch_file,
                          source_line_no=last_patch.source_line_no + 1,
                          applied_line_no=last_patch.applied_line_no + 1)

        self.patches += [new_patch]

    def enable_patch(self, patch_number):
        # should this be defined in entity or plugin?
        raise NotImplementedError

    def disable_patch(self, patch_number):
        raise NotImplementedError

    def register(self, regexp):
        # make sure the function accepts correct args?
        def register(f):
            self.parsers += [LineParser(regexp=regexp, consume=f)]
        return register 

parser = spec()

@parser.register("^\s*Name:\s*(\S+)")
def parse_name(self, name):
    self.name = name

@parser.register("^\s*Version:\s*(\S+)")
def parse_version(self, version):
    self.version = version

@parser.register("^\s*Release:\s*(\S+)")
def parse_release(self, release):
    self.release = release

@parser.register("^\s*Summary:\s*(.+)")
def parse_summary(self, summary):
    self.summary = summary

@parser.register("^\s*Patch(\d+):\s*(.+)")
def parse_patch_definition(self, patch_number, patch_file):
    self.patches += [Patch(patch_number=int(patch_number), source=patch_file,
                           source_line_no=self.line_no, applied_line_no=None)]

@parser.register("^\s*%patch(\d+)\s*(.+)")
def parse_patch_application(self, patch_number, options):
    for p in self.patches:
        if p.patch_number == int(patch_number):
            p.applied_line_no = self.line_no

# ^ These all look the same, maybe make a generic func?
# the regexp are rather similar as well
# but then again the processing will likely be quite different
# so maybe just commot decorator?
