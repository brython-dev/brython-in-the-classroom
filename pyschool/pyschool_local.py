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

sys.path.append('libs')
import CommandHandler
import GoogleDataStore

# port to be used if the server runs locally
if webapp2 is None:
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
    import sys
    sys.path.append('libs')
    import GoogleDataStore

    class MainPage(webapp2.RequestHandler):
        def get(self):
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            self.response.headers['Content-Type'] = 'text/plain'

    class Auth(webapp2.RequestHandler):
        def get(self):
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            _token=GoogleDataStore.Authenticate(userid=self.request.get('userid'),
                                                password=self.request.get('password')) 
            self._response.write('token=%s' % _token)

    class FileStorage(webapp2.RequestHandler):
        def post(self):
            token=self.request.get('token', None)
            if token is None or len(token) < 32:
               self.response.write('invalid token')
               return

            data=self.request.get('data')
            _command=json.loads(data)

            _gds=GoogleDataStore.GoogleDataStore(_command)

            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            self.response.write(_gds.execute_command())

    application = webapp2.WSGIApplication([('/', MainPage), 
                 ('/FS', FileStorage), ('/Auth', Auth)], debug=True)


###############################################################################


if __name__ in '__main__':
    p0rint(__doc__)
    run_local() if not webapp2 else run_on_the_cloud()
