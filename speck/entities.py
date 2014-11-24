class Source():
    def __init__(self, number, source, line_no):
        self.number = number
        self.source = source
        self.line_no = line_no

class Patch():
    def __init__(self, patch_number=None, source=None, source_line_no=None,
                 applied_line_no=None):
        self.patch_number = patch_number
        self.source = source
        self.source_line_no = source_line_no
        self.applied_line_no = applied_line_no

    def __str__(self):
        return ('Patch number {}, stored in {}, '
                'defined at {} and applied at {}'.format(self.patch_number,
                                                         self.source,
                                                         self.source_line_no,
                                                         self.applied_line_no))

class LineParser():
    def __init__(self, regexp=None, consume=None):
        self.regexp = regexp
        self.consume = consume
