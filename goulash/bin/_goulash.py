""" goulash.bin._goulash
"""
import os
from argparse import ArgumentParser

#from fabric.colors import red

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


from goulash.fileserver import main as fileserver
from goulash.projects import version_bump
def project_handler(args):
    if args.version_bump:
        version_bump(args.version_bump)
    else:
        raise SystemExit("unknown project subcommand")

def entry():
    parser = get_parser()
    args = parser.parse_args()
    if args.subcommand in ['version', 'help']:
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
