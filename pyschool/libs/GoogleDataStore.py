import CommandHandler
import FileObject
import hashlib
import time

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
      modified_date = ndb.DateTimeProperty()

def CreateNewAccount(userid, password):
    _users=User.query(User.userid==userid).fetch()
    print '%s' % _user
    if len(_users) != 0:
       #userid already taken
       return json.dumps({'status': 'Error',
                          'message': 'UserID already exists'})
    User(userid=userid, password=password)
    User.put()
    return json.dumps({'status': 'Okay', 'message': 'Account created'})

def Authenticate(userid, password):
    print "Authenticate"
    _users=User.query(User.userid==userid).fetch()
    print '%s' % _user

    assert len(_users) == 1
    _user=_users[0]
    if _user.password == password:
       #create token
       _string="%s:%s:%s" % (userid, password, time.time())
       _token=hashlib.sha1(_string.encode('utf-8')).hexdigest()
       _user.token=_token
       _user.expiration_date = time.time()
       _user.put()
       return _token
       
    return None

class GoogleDataStore(CommandHandler.CommandHandler):
  def __init__(self, request):
      CommandHandler.CommandHandler.__init__(self, request)
      self._token=request.get('token', None)
      #self._userid='earney'
      self._user=User.query(User.token==_token)

  def valid_token(self):
      return self._user.expiration_date < time.time()

  def _list_files(self, directory):
      _files = FileRecord.query(FileRecord.user==self._user.key).fetch()

      _list=[]
      for _file in _files:
          _list.append({'filename': _file.filename, 
                        'modified_date': _file.modified_date})

      return _list

  def _read_file(self, filename):
      _file = FileRecord.query(FileRecord.user==self._user.key,
                               FileRecord.filename==filename).fetch()

      return _file.contents

  def _write_file(self, fileobj):
      _file = FileRecord.query(FileRecord.user==self._user.key,
                               FileRecord.filename==filename).fetch()

      if _file is None:
         _file=FileRecord(user=self._user, filename=fileobj.get_filename(),
                    contents=fileobj.get_attribute('contents'),
                    modified_date=fileobj.get_attribute('modified_date'))
      else:
         #what to do if the file record already exists..
         _file.put()

  def _rm_file(self, filename):
      _file = FileRecord.query(FileRecord.user==self._user.key,
                               FileRecord.filename==filename).fetch()
      _file.delete()

      return True
