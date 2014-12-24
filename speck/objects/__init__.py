class Patch():
    def __init__(self, number=None, source=None, source_line_no=None,
                 applied_line_no=None):
        self.number = number
        self.source = source
        self.source_line_no = source_line_no
        self.applied_line_no = applied_line_no

class Prep():
    def __init__(self, line_no):
        self.line_no = line_no

class Description():
    def __init__(self, line_no):
        self.line_no = line_no

class Build():
    def __init__(self, line_no):
        self.line_no = line_no

class Install():
    def __init__(self, line_no):
        self.line_no = line_no

class Check():
    def __init__(self, line_no):
        self.line_no = line_no

class Source():
    def __init__(self, number, source, line_no):
        self.number = number
        self.source = source
        self.line_no = line_no

class Global():
    def __init__(self, name, value, line_no):
        self.name = name
        self.value = value
        self.line_no = line_no
