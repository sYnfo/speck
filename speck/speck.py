import re
from functools import partial

from .utils import LineParser


class spec():
    parsers = []
    actions = {}

    def __init__(self, type="generic"):
        self.type = type
        self.sources = []
        self.patches = []
        self.globals = []

        from . import parsers
        from . import actions

        for action in spec.actions[type]:
            setattr(self, action, partial(spec.actions[type][action], self))

    def parse(self, spec_file):
        self.spec_file = spec_file
        with open(spec_file, 'r') as f:
            for self.current_line, line in enumerate(f, start=1):
                for p in spec.parsers:
                    match = p.regexp.match(line)
                    if match:
                        p.consume(self, *match.groups())

    # modify patch <number>
    # opens up vim with the patch def and app

    # modyfying e.g. Patch should maybe write it file automatically?

    def add_patch(self, patch_file):
        raise NotImplementedError

    def remove_patch(self, patch_file):
        raise NotImplementedError

    def enable_patch(self, number):
        # should this be defined in entity or plugin?
        raise NotImplementedError

    def disable_patch(self, number):
        raise NotImplementedError

    @staticmethod
    def register_parser(regexp):
        def register_parser(f):
            spec.parsers += [LineParser(regexp=re.compile(regexp), consume=f)]
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

