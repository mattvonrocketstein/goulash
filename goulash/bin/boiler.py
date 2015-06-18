#!/usr/bin/env python
""" goulash.bin.pybpgen
"""

import os
import shutil
from argparse import ArgumentParser
from fabric.colors import red
from fabric import api

from goulash import version
from goulash import goulash_data
from goulash._fabric import require_bin
from goulash._os import touch, makedirs, copy_tree

import sys
import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

def get_parser():
    """ build the default parser """
    parser = ArgumentParser()
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
        msg = red('..docs root ') +\
              '"{0}"'.format(DOCS_ROOT) + \
              red(' does not exist, creating it')
        print msg
        api.local('mkdir -p "{0}"'.format(DOCS_ROOT))
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
    DOCS_ROOT=None,
    DOCS_API_ROOT=None,
    DOCS_SITE_DIR=None, **ctx):
    if os.environ.get('GOULASH_DOCS_API', 'true').lower()=='false':
        print red('skipping API documentation')
        return
    err = ('Missing required command.  '
           '"pip install pdoc" and try again')
    require_bin('pdoc', err)
    cmd = 'pdoc {0} --html --overwrite'
    err = 'refresh requires --project'
    assert PROJECT_NAME is not None, err
    cmd = cmd.format(PROJECT_NAME)
    with api.lcd(DOCS_API_ROOT):
        api.local(cmd)
        src = os.path.join(DOCS_API_ROOT, PROJECT_NAME)
        copy_tree(src, DOCS_API_ROOT)
        shutil.rmtree(os.path.join(DOCS_API_ROOT, PROJECT_NAME))
    if os.path.exists(DOCS_SITE_DIR):
        print red(str([DOCS_API_ROOT, DOCS_SITE_DIR]))
        src = DOCS_API_ROOT
        dest = os.path.join(DOCS_SITE_DIR, 'api')
        copy_tree(src, dest)
        dest = os.path.join(DOCS_ROOT, 'docs', 'api')
        copy_tree(src, dest)
    print red(".. finished generating api docs")

def _create_docs(PROJECT_NAME=None, DOCS_ROOT=None, **ctx):
    mkdocs_config = os.path.join(DOCS_ROOT, 'mkdocs.yml')
    assert PROJECT_NAME is not None
    def dl_bp():
        shutil.copy(
            os.path.join(goulash_data,
                         'mkdocs.yml'),
            mkdocs_config)
        with open(mkdocs_config, 'r') as fhandle:
            tmp = fhandle.read().format(project_name=PROJECT_NAME)
        with open(mkdocs_config, 'w') as fhandle:
            fhandle.write(tmp)
    require_bin('mkdocs',
                'Missing required command.  "pip install mkdocs" and try again')
    print red(".. generating mkdocs: ") + DOCS_ROOT
    if not os.path.exists(DOCS_ROOT):
        msg = red('.. mkdocs dir at "{0}" '.format(DOCS_ROOT)) + \
              red(' does not exist, creating it')
        print msg
        os.mkdir(DOCS_ROOT)
    cmd = ('mkdocs new {0}').format(DOCS_ROOT)
    api.local(cmd)

    print red("creating placeholder for API documentation..")
    makedirs(os.path.join(DOCS_ROOT, 'docs', 'api'))
    touch(os.path.join(DOCS_ROOT, 'docs', 'api', 'index.html'))

    if not os.path.exists(mkdocs_config):
        print red(' .. {0} not found '.format(mkdocs_config))
        print red(' .. no config for docs, using standard boilerplate')
        dl_bp()
    with open(mkdocs_config, 'r') as fhandle:
        if fhandle.read().strip().endswith('My Docs'):
            msg = red(' .. brand new docs!')
            msg += ' using standard boilerplate'
            print msg
            #default_config = True
            dl_bp()
    print red(".. copying custom mkdocs theme")
    from goulash._os import copy_tree
    src = os.path.join(goulash_data, 'glsh')
    dest = os.path.join(DOCS_ROOT, 'glsh')
    copy_tree(src, dest)
    print red(".. refreshing docs")
    _refresh_docs(DOCS_ROOT=DOCS_ROOT, **ctx)
    print red(".. finished with mkdocs")

def _create_api_docs(DOCS_API_ROOT=None, **ctx):
    print red("..generating api documentation to")+" {0}".format(DOCS_API_ROOT)
    if not os.path.exists(DOCS_API_ROOT):
        msg = red('.. api dir at "{0}" '.format(DOCS_API_ROOT))
        msg += red(' does not exist, creating it')
        print msg
        os.mkdir(DOCS_API_ROOT)
    _refresh_api_docs(DOCS_API_ROOT=DOCS_API_ROOT, **ctx)

def _refresh_docs(DOCS_ROOT=None, **ctx):
    with api.lcd(DOCS_ROOT):
        api.local('mkdocs build --clean')

def docs_refresh(**ctx):
    _refresh_docs(**ctx)
    _refresh_api_docs(**ctx)

def docs_deploy(DOCS_ROOT=None, **ctx):
    """ """
    import mkdocs
    from mkdocs.config import load_config
    from mkdocs.gh_deploy import gh_deploy
    mkdocs_config = os.path.join(DOCS_ROOT, 'mkdocs.yml')
    assert os.path.exists(mkdocs_config)
    os.chdir(DOCS_ROOT)
    try:
        config = load_config(
            config_file=mkdocs_config,
        )
        gh_deploy(config)
    except mkdocs.exceptions.ConfigurationError as e:
        # Avoid ugly, unhelpful traceback
        raise SystemExit('\n' + str(e))

def entry():
    parser = get_parser()
    options, args = [parser.parse_args()] * 2
    if args.version:
        print version.__version__
        raise SystemExit()
    elif args.docs:
        gen_docs(args)
if __name__ == '__main__':
    entry()
