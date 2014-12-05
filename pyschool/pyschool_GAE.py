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
import urllib
import urlparse

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
            try:
               _data=json.loads(self.request.body)
            except Exception as e:
               self.response.write(json.dumps({'status': 'Error',
                                               'message': str(e)}))
               return

            _json=_data['data']
            #_json=json.loads(self.request.get('data', None))  #.get('json', None)
            if _json is None:
               #print(self.request)
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
               self.response.write(_gds.execute_command())
               return

            self.response.write(json.dumps({'status': 'Error',
                                            'message': 'invalid token'}))

class Shares(webapp2.RequestHandler):
  def get(self, shareid, path):
      print shareid, path
      #_shareid=self.request.get('shareid', None)
      if shareid is None:
         self.response.write(json.dumps({'status': 'Error', 
                                         'message': 'shareid not supplied'}))
         return

      #_shareid=urllib.unquote(_shareid)

      if path is not None:
      #if '/' in _shareid:  #share used as a directory maybe a package.
         #_shareid, _path = _shareid.split('/', 1)
         _res=GoogleDataStore.GetSharedFile(shareid, path)
         self.response.write(json.dumps(_res))
         return

      #see if this share_id is in database, if so, lookup file and send
      #file contents back to user
      _res=GoogleDataStore.GetSharedFile(shareid)
      self.response.write(json.dumps(_res))

class SharePermissions(webapp2.RequestHandler):
  """ allows user to make directory/file shareable, unshareable.
      also lists files and which ones are shared, not shared
  """
  def post(self):
      #commands, list all files (with shareids).
      # : share file/directory
      # : unshare file/directory
      print self.request.body
      _request=urlparse.parse_qs(self.request.body)
      _sh=GoogleDataStore.ShareHandler(_request)
      if not _sh.valid_token():
         self.response.write(json.dumps({'status': 'Error',
                                         'message': 'Invalid token'}))
         return

      self.response.write(_sh.execute_command())


application = webapp2.WSGIApplication([('/', MainPage), 
                 ('/FS', FileStorage), ('/Auth', Auth),
                 ('/SharePermissions', SharePermissions),
                 #webapp2.Route(r'/Shares/<shareid:[a-h0-9]+>/<path:.*>', handler=Shares),
                 webapp2.Route(r'/Shares/<shareid>/<path>', handler=Shares),
                 ('/CreateUserAccount', CreateUserAccount)], debug=True)
