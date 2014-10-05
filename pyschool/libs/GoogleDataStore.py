import CommandHandler
import FileObject
import hashlib
import time
import json
import datetime

from google.appengine.ext import ndb
# https://cloud.google.com/appengine/docs/python/ndb/

class User(ndb.Model):
      userid=ndb.StringProperty()
      password=ndb.StringProperty()
      token=ndb.StringProperty()
      expiration_date=ndb.DateTimeProperty()

class FileRecord(ndb.Model):
      user = ndb.KeyProperty(kind=User)
      filename = ndb.StringProperty()
      contents = ndb.TextProperty()
      modified_date = ndb.IntegerProperty()

def CreateUserAccount(userid, password):
    _users=User.query(User.userid==userid).fetch()
    if len(_users) != 0:
       #userid already taken
       return json.dumps({'status': 'Error',
                          'message': 'UserID already exists'})
    _user=User(userid=userid, password=password)
    _user.put()
    return {'status': 'Okay', 'message': 'Account created'}

def Authenticate(userid, password):
    _users=User.query(User.userid==userid).fetch()

    if len(_users) != 1:
       return {'status': 'Error', 'message': 'Invalid Userid/Password'}

    _user=_users[0]
    if _user.password == password:
       #create token
       _string="%s:%s:%s" % (userid, password, time.time())
       _token=hashlib.sha1(_string.encode('utf-8')).hexdigest()
       _user.token=_token
       _user.expiration_date = datetime.datetime.fromtimestamp(time.time())
       _user.put()
       return {'status': 'Okay', 'token': _token}
       
    return {'status' :'Error', 'message': 'Invalid Userid/Password'}

class GoogleDataStore(CommandHandler.CommandHandler):
  def __init__(self, request):
      CommandHandler.CommandHandler.__init__(self, request)
      self._token=request.get('token', None)
      _results=User.query(User.token==self._token).fetch()
      if len(_results) == 1:
         self._user=_results[0]
      else:
         self._user=None

  def valid_token(self):
      if self._user is None:
         return False

      return self._user.expiration_date < datetime.datetime.fromtimestamp(time.time())

  def _list_files(self, directory):
      _files = FileRecord.query(FileRecord.user==self._user.key).fetch()

      _list=[]
      for _file in _files:
          _list.append({'filename': _file.filename, 
                        'modified_date': _file.modified_date})

      return {'status': 'Okay', 'filelist': _list}

  def _read_file(self, filename):
      _file = FileRecord.query(FileRecord.user==self._user.key,
                               FileRecord.filename==filename).fetch()

      if len(_file) == 0:
         return json.dumps({'status': 'Error', 'message': 'File does not exist'})
      if len(_file) == 1: 
         return json.dumps({'status': 'Okay', 'fileobj': _file[0].contents})

      return json.dumps({'status': 'Error', 'message': 'Filesystem inconsistent'})
      

  def _write_file(self, fileobj):
      _f=FileObject.FileObject()
      _f.from_json(fileobj)

      _file = FileRecord.query(FileRecord.user==self._user.key,
                               FileRecord.filename==_f.get_filename()).fetch()

      _md=_f.get_attribute('modified_date')
      if _md is None:
         _f.set_attribute('modified_date', 1)

      if len(_file)==1:
         #what to do if the file record already exists..
         _file.contents=_f.to_json()
         _file.modified_date=_f.get_attribute('modified_date')
         _file[0].put()
         return json.dumps({'status': 'Okay', 'message': 'File saved..'})

      print _file
      if len(_file) == 0:
         #file doesn't exist in database, so lets create it a record
         #for it.
         _file=FileRecord(user=self._user.key, filename=_f.get_filename(),
                    contents=fileobj,   # want to save the whole file object
                    modified_date=_f.get_attribute('modified_date'))
         _file.put()
         return json.dumps({'status': 'Okay', 'message': 'File saved..'})

      # more then 1 file.. this shouldn't happen (should return error)
      return json.dumps({'status': 'Error', 'message': 'Error...'})   


  def _rm_file(self, filename):
      _file = FileRecord.query(FileRecord.user==self._user.key,
                               FileRecord.filename==filename).fetch()
      _file.delete()

      return json.dumps({'status': 'Okay', 'message': 'File deleted..'})
