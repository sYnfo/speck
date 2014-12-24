from glob import glob
import sys

import click
from tabulate import tabulate

from .speck import spec
from .utils import input_from_editor

parser = spec()

@click.group()
@click.option('--spec', type=click.Path(exists=True))
def cli(spec):
    """speck"""
    if not spec:
        specs = glob('./*.spec')
        if len(specs) > 1:
            click.echo("Multiple spec file in current directory, "
                       "please specify one")
            sys.exit(1)
        elif len(specs) == 0:
            click.echo("No spec file found in current directory")
            sys.exit(1)
        spec = specs[0]

    parser.parse(spec)

@cli.group()
def patch():
    """manages patches"""

@patch.command("add")
@click.argument("file")
def patch_add(file):
    """adds patch"""
    parser.add_patch(file)

@patch.command("edit")
@click.argument("number")
def patch_edit(number):
    """edits patch"""
    # when no number specified, edit all patches
    # there can be multiple patches with the same number,
    # as long as they're ifed out, careful about that

    # figure out what's the old patch, figure out the new patch
    # let spec worry about everything else

    # it should have non interactive version as well
    patch = filter(lambda p: p.patch_number == int(arguments['<number>']),
                   parser.patches)[0]
    template = ("Patch{number}: {source}\n"
                "%patch{number} {options}").format(number=patch.patch_number,
                                                 source=patch.source,
                                                 options="-p1")
    input = input_from_editor(template)
    p = spec()
    p.parse(input)
    p.modify_patch(number, new_patch)

@patch.command("list")
def patch_list():
    """lists patches"""
    patches = []
    for patch in parser.patches:
        patches += [[patch.number, patch.source]]
    click.echo(tabulate(patches))

@cli.group()
def source():
    """manages patches"""

@source.command("list")
def source_list():
    """lists sources"""
    sources = []
    for source in parser.sources:
        sources += [[source.number, source.source]]
    click.echo(tabulate(sources))
