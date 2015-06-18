#!/usr/bin/env python
""" goulash.bin.pybpgen
"""

import shutil
import os, sys

from argparse import ArgumentParser
from fabric.colors import red
from fabric import api

from goulash import version
from goulash import goulash_data
from goulash.decorators import require_module

def get_parser():
    """ build the default parser """
    parser = ArgumentParser()
    #parser.set_conflict_handler("resolve")
    parser.add_argument(
        "--docs", default=False, dest='docs',
        action='store_true',
        help=("create docs boilerplate for python project"))
    parser.add_argument(
        "--project", default='', dest='project',
        required=True,
        help=("project name"))
    parser.add_argument(
        'dir', nargs='?', default=os.getcwd(),
        help=("base directory to generate boilerplate in"))
    parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    return parser

def gen_docs(args):
    print red('generating docs boilerplate..')
    SRC_ROOT = args.dir
    DOCS_ROOT = os.path.join(SRC_ROOT, 'docs')
    DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
    DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')
    PROJECT_NAME = args.project
    ctx = locals().copy()
    ctx.pop('args')
    create_docs(**ctx)

def create_docs(DOCS_ROOT=None, **ctx):
    """ """
    if not os.path.exists(DOCS_ROOT):
        msg = red('..docs root ')+\
              '"{0}"'.format(DOCS_ROOT)+ \
              red(' does not exist, creating it')
        print msg
        os.mkdir(DOCS_ROOT)
    else:
        msg = '.. docs root already exists:'
        print red(msg) + ' {0}'.format(DOCS_ROOT)
    shutil.copy(
        os.path.join(goulash_data, 'docs_requirements.txt'),
        os.path.join(DOCS_ROOT, 'requirements.txt'))
    _create_docs(DOCS_ROOT=DOCS_ROOT, **ctx)
    _create_api_docs(DOCS_ROOT=DOCS_ROOT, **ctx)

def _refresh_api_docs(
    PROJECT_NAME=None,
    DOCS_API_ROOT=None,
    DOCS_SITE_DIR=None, **ctx):
    if os.environ.get('GOULASH_DOCS_API', 'true').lower()=='false':
        print red('skipping API documentation')
        return
    cmd = ('epydoc ./{0} --html -q -o {1} '
           '--name {2} --css blue '
           '--show-imports --inheritance listed')
    default_md5 = '6bc2c4f724ccc3bacbb77cf8a46963d1'
    assert PROJECT_NAME is not None, 'refresh requires --project'
    cmd = cmd.format(PROJECT_NAME, DOCS_API_ROOT, PROJECT_NAME)
    api.local(cmd)
    with api.lcd(DOCS_API_ROOT):
        md5_cmd = 'md5sum {0}'.format('epydoc.css')
        md5_val = api.local(md5_cmd, capture=True).strip().split()[0]
        if md5_val == default_md5:
            print red(' .. found default epydoc.css, '
                'copying standard boilerplate')
            shutil.copy(
                os.path.join(goulash_data, 'epydoc.css'),
                os.path.join(DOCS_API_ROOT,'epydoc.css'))
        else:
            red(" .. standard epydoc.css boilerplate has already been fetched")
    if os.path.exists(DOCS_SITE_DIR):
        shutil.rmtree(os.path.join(DOCS_SITE_DIR, 'api'))
        api.local('mv {0} {1}'.format(
            DOCS_API_ROOT, DOCS_SITE_DIR))
    print red(".. finished generating epydoc")

#@require_module('mkdocs', exception=RuntimeError)
def _create_docs(PROJECT_NAME=None, DOCS_ROOT=None, **ctx):
    mkdocs_config = os.path.join(DOCS_ROOT, 'mkdocs.yml')
    assert PROJECT_NAME
    def dl_bp():
        shutil.copy(
            os.path.join(goulash_data,
                         'mkdocs.yml'),
            mkdocs_config)
        with open(mkdocs_config, 'r') as fhandle:
            tmp = fhandle.read().format(project_name=PROJECT_NAME)
        with open(mkdocs_config, 'w') as fhandle:
            fhandle.write(tmp)

    print red(".. generating mkdocs: ")+DOCS_ROOT
    if not os.path.exists(DOCS_ROOT):
        msg = red('.. mkdocs dir at "{0}" '.format(DOCS_ROOT)) + \
              red(' does not exist, creating it')
        print msg
        os.mkdir(DOCS_ROOT)
    cmd = ('mkdocs new {0}').format(DOCS_ROOT)
    api.local(cmd)
    with api.lcd(DOCS_ROOT):
        api.local('mkdir -p docs/api')
        api.local('touch docs/api/index.html')
    if not os.path.exists(mkdocs_config):
        print red(' .. {0} not found '.format(mkdocs_config))
        print red(' .. no config for docs, downloading standard boilerplate')
        dl_bp()
    with open(mkdocs_config, 'r') as fhandle:
        if fhandle.read().strip().endswith('My Docs'):
            print red(' .. brand new docs!')+\
                  ' downloading standard boilerplate'
            default_config = True
            dl_bp()
    print red(".. triggering first docs build")
    _refresh_docs(DOCS_ROOT=DOCS_ROOT, **ctx)
    print red(".. finished generating mkdocs")

def _create_api_docs(DOCS_API_ROOT=None, **ctx):
    print red("..generating epydoc to")+" {0}".format(DOCS_API_ROOT)
    if not os.path.exists(DOCS_API_ROOT):
        msg = red('..epydoc dir at "{0}" '.format(DOCS_API_ROOT)) + \
              red(' does not exist, creating it')
        print msg
        os.mkdir(DOCS_API_ROOT)
    _refresh_api_docs(DOCS_API_ROOT=DOCS_API_ROOT, **ctx)

def _refresh_docs(DOCS_ROOT=None, **ctx):
    with api.lcd(DOCS_ROOT):
        api.local('mkdocs build')

def docs_refresh(**ctx):
    _refresh_docs(**ctx)
    _refresh_api_docs(**ctx)

def entry():
    parser = get_parser()
    options, args = [get_parser().parse_args()]*2
    if args.version:
        print version.__version__
        raise SystemExit()
    elif args.docs:
        gen_docs(args)
if __name__=='__main__':
    entry()
