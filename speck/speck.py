import re
from functools import partial

from .entities import LineParser, Prep, Patch, Source


class spec():
    parsers = []
    actions = {}

    def __init__(self, type="generic"):
        self.patches = []
        self.type = type
        for action in spec.actions[type]:
            setattr(self, action, partial(spec.actions[type][action], self))

    def parse(self, spec_file):
        self.spec_file = spec_file
        with open(spec_file, 'r') as f:
            for self.line_no, line in enumerate(f, start=1):
                for p in spec.parsers:
                    match = re.match(p.regexp, line)
                    if match:
                        p.consume(self, *match.groups())

    # modify patch <number>
    # opens up vim with the patch def and app

    # modyfying e.g. Patch should maybe write it file automatically?

    def add_patch(self, patch_file):
        raise NotImplementedError

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

    @staticmethod
    def register_action(binding, type):
        # action has to be a method of spec
        # there should be a way to call the "generic" action,
        # after a specialized one
        def register_parser(f):
            if type not in spec.actions:
                spec.actions[type] = {}
            spec.actions[type][binding.__name__] = f
        return register_parser 

from . import actions


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
