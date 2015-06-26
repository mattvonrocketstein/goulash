""" goulash.boiler
"""
import shutil
import os

from fabric import api
from fabric.colors import red

from goulash._inspect import _main_package
from goulash import goulash_data
from goulash._os import touch, makedirs
from goulash.decorators import require_bin
from goulash.docs import _refresh_docs, _refresh_api_docs

def gen_docs(args):
    print red('generating docs boilerplate..')
    SRC_ROOT = args.dir or '.'
    DOCS_ROOT = os.path.join(SRC_ROOT, 'docs')
    DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
    DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')
    PROJECT_NAME = _main_package(SRC_ROOT)
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
    msg = red("..generating api documentation to")
    msg += " {0}".format(DOCS_API_ROOT)
    print msg
    if not os.path.exists(DOCS_API_ROOT):
        msg = red('.. api dir at "{0}" '.format(DOCS_API_ROOT))
        msg += red(' does not exist, creating it')
        print msg
        os.mkdir(DOCS_API_ROOT)
    _refresh_api_docs(DOCS_API_ROOT=DOCS_API_ROOT, **ctx)

def boiler_handler():
    if args.docs:
        gen_docs(args)
