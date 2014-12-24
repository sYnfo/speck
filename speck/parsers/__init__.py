from speck import spec
from speck.objects import Prep, Description, Build, Install, Check, Source, Patch, Global


@spec.register_parser("^\s*Name:\s*(\S+)")
def parse_name(parser, name):
    parser.name = name

@spec.register_parser("^\s*%prep")
def parse_prep(parser):
    parser.prep = Prep(parser.current_line)

@spec.register_parser("^\s*%description")
def parse_description(parser):
    parser.description = Description(parser.current_line)

@spec.register_parser("^\s*%build")
def parse_build(parser):
    parser.build = Build(parser.current_line)

@spec.register_parser("^\s*%install")
def parse_install(parser):
    parser.install = Install(parser.current_line)

@spec.register_parser("^\s*%check")
def parse_check(parser):
    parser.check = Check(parser.current_line)

@spec.register_parser("^\s*Release:\s*(\S+)")
def parse_release(parser, release):
    parser.release = release

@spec.register_parser("^\s*Source(\d+):\s*(\S+)")
def parse_source(parser, number, source):
    parser.sources.append(Source(int(number), source, parser.current_line))

@spec.register_parser("^\s*Version:\s*(\S+)")
def parse_version(parser, version):
    parser.version = version

@spec.register_parser("^\s*Patch(\d+):\s*(.+)")
def parse_patch_definition(parser, number, source):
    parser.patches.append(Patch(number=int(number),
                                source=source,
                                source_line_no=parser.current_line,
                                applied_line_no=None))

@spec.register_parser("^\s*%patch(\d+)\s*(.+)") 
def parse_patch_application(parser, number, options):
    for p in parser.patches:
        if p.number == int(number):
            p.applied_line_no = parser.current_line

@spec.register_parser("^\s*Summary:\s*(.+)")
def parse_summary(parser, summary):
    parser.summary = summary

@spec.register_parser("^\s*License:\s*(.+)")
def parse_summary(parser, license):
    parser.license = license

@spec.register_parser("^\s*URL:\s*(.+)")
def parse_summary(parser, URL):
    parser.URL = URL

@spec.register_parser("^\s*BuildArch:\s*(.+)")
def parse_summary(parser, buildarch):
    parser.buildarch = buildarch

@spec.register_parser("^\s*%global\s+(\S+)\s+(\S+)")
def parse_summary(parser, name, value):
    parser.globals.append(Global(name, value, parser.current_line))
