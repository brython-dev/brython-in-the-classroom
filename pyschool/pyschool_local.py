# -*- coding: utf-8 -*-
#

"""Simple server that uses Local Pythons BaseHTTPServer.

To start pyschool locally just run:

> python pyschool_local.py --port 8001

The --port option is only necessary if you want to run the local server
on a port different than 8000.

It can bu used with python >= 2.7
"""

# imports
import sys
import os
import argparse


# port to be used when the server runs locally
parser = argparse.ArgumentParser()
parser.add_argument('--port', 
    help="The port to be used by the local server")
args = parser.parse_args()

if args.port:
    port = int(args.port)
else:
    port = 8000


def run_local():
    """This function runs a basic builtin server locally for development."""
    try:
        os.nice(19)
    except Exception as error:
        print(error)
    if sys.version_info[0] < 3:
        import BaseHTTPServer as server
        from CGIHTTPServer import CGIHTTPRequestHandler
    else:
        import http.server as server
        from http.server import CGIHTTPRequestHandler
    server_address, handler = ('', port), CGIHTTPRequestHandler
    httpd = server.HTTPServer(server_address, handler)
    print(("""Server running on port http://localhost:{}.
           """.format(server_address[1])))
    httpd.serve_forever()


if __name__ in '__main__':
    run_local()
