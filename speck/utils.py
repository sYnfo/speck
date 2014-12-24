import tempfile
import os
import subprocess


def input_from_editor(template):
    editor = os.environ.get('EDITOR', 'vim')

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tmp:
        tmp.write(template)
        tmp.flush()
        subprocess.call([editor, tmp.name])
        tmp.seek(0)
        return tmp.readlines()

class LineParser():
    def __init__(self, regexp=None, consume=None):
        self.regexp = regexp
        self.consume = consume
