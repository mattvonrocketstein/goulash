""" goulash.projects
"""

import os
from fabric.colors import red

VERSION_DELTA = .01

def project_search(fname, start=None):
    """ project-based directory tree search, where if the taget file
    isn't found in the working directory then you proceed upward until
    the file is found or you hit the file-system root. useful for
    project-style rc configuration data, say .git or .ackrc, etc.
    """
    start = start or os.getcwd()
    start = os.path.abspath(start)
    now = start
    while True:
        if fname in os.listdir(now):
            return os.path.join(now, fname)
        if os.path.dirname(now) == now:
            return None # reached the root
        now = os.path.dirname(now)

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
