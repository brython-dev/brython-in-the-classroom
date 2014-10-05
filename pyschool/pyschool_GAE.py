# -*- coding: utf-8 -*-
#


"""Simple server that uses Google App Engine to run pyschool.

Only Python 2.7
"""


# imports
import sys
import os
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

            _res=GoogleDataStore.Authenticate(userid=_userid,
                                              password=_password) 
            self.response.write(json.dumps(_res))

class CreateUserAccount(webapp2.RequestHandler):
        def get(self):
            self.response.headers.add_header("Access-Control-Allow-Origin", "*")
            _userid=self.request.get('userid', None)
            _password=self.request.get('password', None)
            if _userid is None or _password is None:
               self.response.write(json.dumps({'status': 'Error',
                                            'message': 'invalid userid/password'}))
               return

            _res=GoogleDataStore.CreateUserAccount(userid=_userid,
                                                   password=_password) 
            self.response.write(json.dumps(_res))

class FileStorage(webapp2.RequestHandler):
        def post(self):
            
            #there is probably something wrong with brythons' ajax
            #function that causes the post data to be part of the body
            _data=json.loads(self.request.body)
            _json=_data['data']
            #_json=json.loads(self.request.get('data', None))  #.get('json', None)
            if _json is None:
               print(self.request)
               self.response.write(json.dumps({'status': 'Error',
                                               'message': 'invalid message'}))
               return

            _token=_json['token']
            if _token is None or len(_token) < 32:
               self.response.write(json.dumps({'status': 'Error',
                                               'message': 'invalid token'}))
               return

            _gds=GoogleDataStore.GoogleDataStore(_json)
            if _gds.valid_token():
               self.response.headers.add_header("Access-Control-Allow-Origin", "*")
               self.response.write(_gds.execute_command())
               return

            self.response.write(json.dumps({'status': 'Error',
                                            'message': 'invalid token'}))

application = webapp2.WSGIApplication([('/', MainPage), 
                 ('/FS', FileStorage), ('/Auth', Auth),
                 ('/CreateUserAccount', CreateUserAccount)], debug=True)
