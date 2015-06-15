#!/usr/bin/env python
""" goulash.bin.docs
"""

import shutil
import os, sys
import webbrowser

from argparse import ArgumentParser
from fabric.colors import red
from fabric import api

from goulash import version
from goulash import goulash_data
from goulash.decorators import require_module
from goulash.bin.boiler import gen_docs, docs_refresh

def _get_ctx(args):
    SRC_ROOT = os.path.dirname(args.dir)
    DOCS_ROOT = os.path.join(SRC_ROOT, 'docs')
    DOCS_URL = 'http://localhost:8000'
    DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
    DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')
    PROJECT_NAME = args.project
    ctx = locals().copy()
    ctx.pop('args')
    return ctx

def refresh(args):
    print red('refreshing docs..')
    docs_refresh(**_get_ctx(args))

def show(args):
    refresh(args)
    ctx = _get_ctx(args)
    if 'docs' in os.listdir(ctx['DOCS_ROOT']):
        print red('.. found read-the-docs style documentation')
        with api.lcd(ctx['DOCS_SITE_DIR']):
            webbrowser.open(ctx['DOCS_URL'])
            api.local('goulash-serve')#from goulash.bin.serv import run_server
            #run_server(dir=ctx['DOCS_SITE_DIR'])
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
        required=True,
        help=("project name"))
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
        'dir', nargs='?', default='docs',
        help=("base directory for docs"))
    parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    return parser

def entry():
    parser = get_parser()
    args = get_parser().parse_args()
    if args.version:
        print version.__version__
        raise SystemExit()
    elif args.boilerplate:
        args.dir = os.path.dirname(args.dir)
        return gen_docs(args)
    elif args.refresh:
        return refresh(args)
    elif args.show:
        return show(args)

if __name__=='__main__':
    entry()
