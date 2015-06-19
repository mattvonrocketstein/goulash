""" goulash.bin._goulash
"""
import os
from argparse import ArgumentParser

#from fabric.colors import red

from goulash import version
from goulash.fileserver import main as fileserver
from goulash.projects import version_bump, pypi_publish

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
    project_parser.add_argument(
        '-b', default=False, action='store_true',
        dest='version_bump',
        help=("bump version for pkg_root"))
    project_parser.add_argument(
        '--pypi-publish', default=False,
        action='store_true',
        dest='pypi_publish',
        help=("refresh pypi"))

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

    docs_parser = subparsers.add_parser(
        'docs', help='utilities for documentation')
    docs_parser.set_defaults(subcommand='docs')
    docs_parser.add_argument(
        "--boiler-plate", '-b', default=False, dest='boilerplate',
        action='store_true',
        help=("create docs boilerplate for a python project"))
    #docs_parser.add_argument(
    #    "--project", '-p', default='', dest='project',
    #    help=("Specifies project name (required if $PROJECT_NAME is not set)"))
    docs_parser.add_argument(
        "--refresh", '-r',
        default=False, dest='refresh',
        action='store_true',
        help=("refresh this projects documentation"))
    docs_parser.add_argument(
        "--show", '-s',
        default=False, dest='show',
        action='store_true',
        help=("show this projects documentation"))
    docs_parser.add_argument(
        '--deploy',
        default=False,
        dest='deploy', action='store_true',
        help='like mkdocs deploy')
    docs_parser.add_argument(
        'docroot', nargs='?', default='docs',
        help=("base directory for docs"))
    docs_parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))


    return parser


def project_handler(args):
    if args.version_bump:
        version_bump()
    elif args.pypi_publish:
        pypi_publish()
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
    elif args.subcommand == 'docs':
        docs_handler(args)
    else:
        raise SystemExit('unknown subcommand')


import os
import webbrowser

from argparse import ArgumentParser
from fabric.colors import red
from fabric import api

from goulash import version
from goulash._inspect import _main_package
from goulash.fileserver import runserver as fileserver
from goulash.bin.boiler import gen_docs, docs_refresh, docs_deploy

def _get_ctx(args):
    args.docroot = os.path.abspath(args.docroot)
    DOCS_ROOT = args.docroot
    SRC_ROOT = os.path.dirname(args.docroot)
    DOCS_URL = 'http://localhost:8000'
    DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
    DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')
    PROJECT_NAME = _main_package(SRC_ROOT)
    ctx = locals().copy()
    ctx.pop('args')
    #raise Exception,ctx
    return ctx

def refresh(args):
    print red('refreshing docs..')
    docs_refresh(**_get_ctx(args))

def deploy(args):
    print red('deploying docs..')
    docs_deploy(**_get_ctx(args))

def handle_show(args):
    refresh(args)
    ctx = _get_ctx(args)
    if 'docs' in os.listdir(ctx['DOCS_ROOT']):
        print red('.. found read-the-docs style documentation')
        import webbrowser
        webbrowser.open('http://localhost:8000')
        fileserver(dir=os.path.join(args.docroot,'site'))#, port=args.port)

    else:
        print red("Not sure what to do with this style of documentation")

def docs_handler(args):
    """ """
    if args.version:
        print version.__version__
        raise SystemExit()
    elif args.boilerplate:
        args.docroot = os.path.dirname(args.docroot)
        args.dir = os.path.dirname(args.docroot)
        return gen_docs(args)
    elif args.refresh:
        return refresh(args)
    elif args.deploy:
        return deploy(args)
    elif args.show:
        return handle_show(args)
