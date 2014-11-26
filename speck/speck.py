import re

from .entities import LineParser, Prep, Patch, Source

class spec():
    parsers = []

    def __init__(self):
        self.patches = []

    def parse(self, spec_file):
        self.spec_file = spec_file
        with open(spec_file, 'r') as f:
            for self.line_no, line in enumerate(f, start=1):
                for p in spec.parsers:
                    match = re.match(p.regexp, line)
                    if match:
                        p.consume(self, *match.groups())

    # do not implement this in the parser, should be in a plugin
    def add_patch(self, patch_file):
        if self.patches:
            last_patch = sorted(self.patches, key=lambda x: x.source_line_no)[-1]
            new_source_line = last_patch.source_line_no + 1
            new_apply_line = last_patch.applied_line_no + 1
            new_patch_number = last_patch.patch_number + 1
        else:
            new_source_line = self.source.line_no + 1
            new_apply_line = self.prep.line_no + 1
            new_patch_number = 0

        with open(self.spec_file, 'rw') as s:
            lines = s.readlines()
            lines.insert(new_source_line, "Patch{}: {}\n".format(new_patch_number, patch_file))
            lines.insert(new_apply_line, "%patch{} -p1\n".format(new_patch_number))

        with open(self.spec_file, 'w') as s:
            s.writelines(lines)

        new_patch = Patch(patch_number=new_patch_number,
                          source=patch_file,
                          source_line_no=new_source_line,
                          applied_line_no=new_apply_line)

        self.patches += [new_patch]

    def enable_patch(self, patch_number):
        # should this be defined in entity or plugin?
        raise NotImplementedError

    def disable_patch(self, patch_number):
        raise NotImplementedError

    @staticmethod
    def register_parser(regexp):
        def register_parser(f):
            spec.parsers += [LineParser(regexp=regexp, consume=f)]
        return register_parser 

    def register_action(self, noun, verb):
        # make sure the function accepts correct args?
        def register_parser(f):
            #self.add_patch = f
            pass
        return register_parser 

parser = spec()

@spec.register_parser("^\s*%prep")
def parse_prep(self):
    self.prep = Prep(self.line_no)

@spec.register_parser("^\s*Name:\s*(\S+)")
def parse_name(self, name):
    self.name = name

@spec.register_parser("^\s*Version:\s*(\S+)")
def parse_version(self, version):
    self.version = version

@spec.register_parser("^\s*Release:\s*(\S+)")
def parse_release(self, release):
    self.release = release

@spec.register_parser("^\s*Summary:\s*(.+)")
def parse_summary(self, summary):
    self.summary = summary

@spec.register_parser("^\s*Source(\d+):\s*(\S+)")
def parse_source(self, number, source):
    self.source = Source(int(number), source, self.line_no)

@spec.register_parser("^\s*Patch(\d+):\s*(.+)")
def parse_patch_definition(self, patch_number, patch_file):
    self.patches += [Patch(patch_number=int(patch_number), source=patch_file,
                           source_line_no=self.line_no, applied_line_no=None)]

# keep indent
@spec.register_parser("^\s*%patch(\d+)\s*(.+)")
def parse_patch_application(self, patch_number, options):
    for p in self.patches:
        if p.patch_number == int(patch_number):
            p.applied_line_no = self.line_no

# ^ These all look the same, maybe make a generic func?
# the regexp are rather similar as well
# but then again the processing will likely be quite different
# so maybe just commot decorator?
