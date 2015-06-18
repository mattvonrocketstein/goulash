#!/usr/bin/env python
""" goulash.bin.docs
"""

import os
import webbrowser

from argparse import ArgumentParser
from fabric.colors import red
from fabric import api

from goulash import version
from goulash.bin.boiler import gen_docs, docs_refresh, docs_deploy

def _get_ctx(args):
    args.docroot = os.path.abspath(args.docroot)
    DOCS_ROOT = args.docroot
    SRC_ROOT = os.path.dirname(args.docroot)

    DOCS_URL = 'http://localhost:8000'
    DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
    DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')
    PROJECT_NAME = args.project
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

def show(args):
    refresh(args)
    ctx = _get_ctx(args)
    if 'docs' in os.listdir(ctx['DOCS_ROOT']):
        print red('.. found read-the-docs style documentation')
        with api.lcd(ctx['DOCS_SITE_DIR']):
            webbrowser.open(ctx['DOCS_URL'])
            api.local('goulash-serve')
    else:
        print red("Not sure what to do with this style of documentation")

def get_parser():
    """ build the default parser """
    parser = ArgumentParser()
    #parser.set_conflict_handler("resolve")
    parser.add_argument(
        "--boiler-plate", '-b', default=False, dest='boilerplate',
        action='store_true',
        help=("create docs boilerplate for a python project"))
    parser.add_argument(
        "--project", '-p', default='', dest='project',
        help=("Specifies project name (required if $PROJECT_NAME is not set)"))
    parser.add_argument(
        "--refresh", '-r',
        default=False, dest='refresh',
        action='store_true',
        help=("refresh this projects documentation"))
    parser.add_argument(
        "--show", '-s',
        default=False, dest='show',
        action='store_true',
        help=("show this projects documentation"))
    parser.add_argument(
        '--deploy',
        default=False,
        dest='deploy', action='store_true',
        help='like mkdocs deploy')
    parser.add_argument(
        'docroot', nargs='?', default='docs',
        help=("base directory for docs"))
    parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    return parser

def entry():
    parser = get_parser()
    args = parser.parse_args()
    if not os.environ.get('GOULASH_PROJECT'):
        if not args.project:
            err = ("Expected GOULASH_PROJECT would be set, "
                   "or --project would be passed at command line.")
            raise SystemExit(err)
    args.project = args.project if args.project else \
                   os.environ['GOULASH_PROJECT']
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
        return show(args)

if __name__ == '__main__':
    entry()
