#!/usr/bin/env python
""" goulash.bin.serv
"""
# SOURCE:
#  http://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python
import os, sys
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
import SimpleHTTPServer

from argparse import ArgumentParser
from fabric.colors import red

from goulash import version

def get_parser():
    """ build the default parser """
    parser = ArgumentParser()
    #parser.set_conflict_handler("resolve")
    parser.add_argument(
        "--port", default='', dest='port',
        help=("port for http server"))
    parser.add_argument(
        "-v", '--version', default=False, dest='version',
        action='store_true',
        help=("show version information"))
    parser.add_argument(
        'dir', nargs='?', default=os.getcwd(),
        help=("directory to serve files from"))
    return parser

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def main(args):
    port = int(args.port) if args.port else 8000
    _dir = args.dir if args.dir else os.getcwd()
    if not os.path.exists(_dir):
        err = "cannot serve nonexistent directory: {0}".format(_dir)
        raise SystemExit(err)
    os.chdir(_dir)
    msg = "starting file server. port is {0}, directory is {1}"
    msg = msg.format(port, _dir)
    print red(msg)
    server = ThreadingSimpleServer(
        ('', port),
        SimpleHTTPServer.SimpleHTTPRequestHandler)
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print "Finished"

def entry(dir=None):
    parser = get_parser()
    args = parser.parse_args()
    if dir:
        args.dir = dir
    if args.version:
        print version.__version__
        raise SystemExit()
    else:
        main(args)
runserver = run_server = entry

if __name__ == '__main__':
    entry()
