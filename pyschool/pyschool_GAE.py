# -*- coding: utf-8 -*-
#


"""Simple server that uses Google App Engine to run pyschool.

Only Python 2.7
"""


# imports
import sys
import json

import webapp2

sys.path.append('libs')
import CommandHandler
import GoogleDataStore


class MainPage(webapp2.RequestHandler):
        def get(self):
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            self.response.headers['Content-Type'] = 'text/plain'

class Auth(webapp2.RequestHandler):
        def get(self):
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            _userid=self.request.get('userid', None)
            _password=self.request.get('password', None)
            if _userid is None or _password is None:
               self.response.write(json.dumps({'status': 'Error',
                                            'message': 'invalid userid/password'}))
               return

            _token=GoogleDataStore.Authenticate(userid=_userid,
                                                password=_password) 
            self.response.write(json.dumps({'status': 'Okay', 
                                            'token': _token}))

class CreateUserAccount(webapp2.RequestHandler):
        def get(self):
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            _userid=self.request.get('userid', None)
            _password=self.request.get('password', None)
            if _userid is None or _password is None:
               self.response.write(json.dumps({'status': 'Error',
                                            'message': 'invalid userid/password'}))
               return

            _response=GoogleDataStore.CreateUserAccount(userid=_userid,
                                                        password=_password) 
            self.response.write(_response)

class FileStorage(webapp2.RequestHandler):
        def post(self):
            token=self.request.get('token', None)
            if token is None or len(token) < 32:
               self.response.write(json.dumps({'status': 'Error',
                                               'message': 'invalid token'}))
               return

            data=self.request.get('data')
            _command=json.loads(data)

            _gds=GoogleDataStore.GoogleDataStore(_command)
            if _gds.valid_token():
               self.response.headers.add_header("Access-Control-Allow-Origin", "*")
               self.response.write(_gds.execute_command())
               return

            self.response.write(json.dumps({'status': 'Error',
                                            'message': 'invalid token'}))

application = webapp2.WSGIApplication([('/', MainPage), 
                 ('/FS', FileStorage), ('/Auth', Auth),
                 ('/CreateUserAccount', CreateUserAccount)], debug=True)
