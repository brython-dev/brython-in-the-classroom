# -*- coding: utf-8 -*-
#


"""Simple server that uses Google App Or Local Pythons BaseHTTPServer."""


# imports
import sys
import os
import argparse

try:
    import webapp2
except Exception as error:
    webapp2 = None
    print(error)

# port to be used if the server runs locally
parser = argparse.ArgumentParser()
parser.add_argument('--port', 
    help="The port to be used by the local server")
args = parser.parse_args()

if args.port:
	port = int(args.port)
else:
	port = 8000


###############################################################################


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


def run_on_the_cloud():
    """This function runs a Google App server on the cloud for development."""
    class MainPage(webapp2.RequestHandler):
        def get(self):
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            self.response.headers['Content-Type'] = 'text/plain'

    application = webapp2.WSGIApplication([('/', MainPage), ], debug=True)


###############################################################################


if __name__ in '__main__':
    print(__doc__)
    run_local() if not webapp2 else run_on_the_cloud()
