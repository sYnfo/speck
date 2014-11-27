from .speck import spec
from .entities import Patch


@spec.register_action(spec.add_patch, "generic")
def add_patch(spec, patch_file):
    if spec.patches:
        last_patch = sorted(spec.patches, key=lambda x: x.source_line_no)[-1]
        new_source_line = last_patch.source_line_no + 1
        new_apply_line = last_patch.applied_line_no + 1
        new_patch_number = last_patch.patch_number + 1
    else:
        # there can be more sources, pick the last one
        # this seem to be a common theme ^
        new_source_line = spec.source.line_no + 1
        new_apply_line = spec.prep.line_no + 1
        new_patch_number = 0

    with open(spec.spec_file, 'r') as s:
        lines = s.readlines()
        lines.insert(new_source_line, "Patch{}: {}\n".format(new_patch_number,
                                                             patch_file))
        lines.insert(new_apply_line, "%patch{} -p1\n".format(new_patch_number))

    with open(spec.spec_file, 'w') as s:
        s.writelines(lines)

    new_patch = Patch(patch_number=new_patch_number,
                      source=patch_file,
                      source_line_no=new_source_line,
                      applied_line_no=new_apply_line)

    spec.patches += [new_patch]
