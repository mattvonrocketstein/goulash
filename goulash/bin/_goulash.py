""" goulash.bin._goulash
"""
import os
from argparse import ArgumentParser

from fabric.colors import red
from fabric.contrib.console import confirm

from goulash import version

def get_parser():
    """ build the default parser """
    parser = ArgumentParser()
    #parser.set_conflict_handler("resolve")
    parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    subparsers = parser.add_subparsers(help='commands')

    help_parser = subparsers.add_parser('help', help='show help info')
    help_parser.set_defaults(subcommand='help')

    version_parser = subparsers.add_parser(
        'version', help='show goulash version')
    version_parser.set_defaults(subcommand='version')

    project_parser = subparsers.add_parser(
        'project', help='project based subcommands')
    project_parser.set_defaults(subcommand='project')
    #project_parser.add_argument('-f','--force', action='store_true',
    #               help='force noninteractive mode')
    project_parser.add_argument(
        '-b', default=os.getcwd(),
        metavar='pkg_root', dest='version_bump',
        help=("bump version for pkg_root"))

    serve_parser = subparsers.add_parser(
        'serve', help='simple threaded directory-indexing http server')
    serve_parser.set_defaults(subcommand='serve')
    serve_parser.add_argument(
        "--port", default='', dest='port',
        help=("port for http server"))
    serve_parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    serve_parser.add_argument(
        'dir', nargs='?', default=os.getcwd(),
        help=("directory to serve files from"))

    return parser

VERSION_DELTA = .01

def version_bump(pkg_root):
    """ bump the version number.

        to work, this function requires your version file to work like so:

            1. pkg/version.py exists
            2. pkg/version.py contains a '__version__' variable
            3. __version__ should be a number, not a string
            4. __version__ should be defined on the last line of the file
    """
    sandbox = {}
    version_file = os.path.join(pkg_root, 'version.py')
    err = 'Version file not found in expected location: ' + version_file
    if not os.path.exists(version_file):
        raise SystemExit(err)
    execfile(version_file, sandbox)
    current_version = sandbox['__version__']
    new_version = current_version + VERSION_DELTA
    with open(version_file, 'r') as fhandle:
        version_file_contents = [x for x in fhandle.readlines() if x.strip()]
    new_file = version_file_contents[:-1] + \
               ["__version__ = version = {0}".format(new_version)]
    new_file = '\n'.join(new_file)
    print red("warning:") + " version will be changed to {0}".format(new_version)
    print
    print red("new version file will look like this:\n")
    print new_file
    ans = confirm('proceed with version change?')
    if not ans:
        print 'aborting.'
        return
    with open(version_file, 'w') as fhandle:
        fhandle.write(new_file)
        print 'version has been rewritten.'

from goulash.fileserver import main as fileserver

def project_handler(args):
    if args.version_bump:
        version_bump(args.version_bump)
    else:
        raise SystemExit("unknown project subcommand")

def entry():
    parser = get_parser()
    args = parser.parse_args()
    if args.subcommand in ['version','help']:
        if args.subcommand == 'version':
            print version.__version__
        if args.subcommand == 'help':
            parser.print_help()
        raise SystemExit()
    elif args.subcommand == 'project':
        project_handler(args)
    elif args.subcommand == 'serve':
        fileserver(args)
    else:
        raise SystemExit('unknown subcommand')
