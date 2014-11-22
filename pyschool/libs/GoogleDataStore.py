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

class ShareRecord(ndb.Model):
      shareid=ndb.StringProperty()
      user=ndb.KeyProperty(kind=User)
      dir=ndb.StringProperty()
      active=ndb.BooleanProperty()

      is_saved = False

      def _post_put_hook(self, f):
          if f.state == f.FINISHING:
             self.is_saved = True
          else:
             self.is_saved = False

def CreateUserAccount(userid, password):
    _users=User.query(User.userid==userid).fetch()
    if len(_users) != 0:
       #userid already taken
       return {'status': 'Error',
               'message': 'UserID already exists'}
    _user=User(userid=userid, password=password)
    _user.put()
    return {'status': 'Okay', 'message': 'Account created'}

def GetSharedFile(shareid, additional_path=''):
    _sr=ShareRecord.query(ShareRecord.shareid==shareid).fetch()

    if len(_sr) == 0:
       return {'status': 'Error', 'fileobj': None}

    if len(_sr)==1:
       _sr1=_sr[0]
       if not _sr[0].dir.startswith('/pyschool'):
          _filename='/pyschool'+_sr[0].dir
       else:
          _filename=_sr[0].dir

       if additional_path != '':
          _filename+='/' + additional_path
       print _filename
       _fr=FileRecord.query(FileRecord.filename==_filename).fetch()

       if len(_fr) == 1:
          return {'status': 'Okay', 'fileobj': _fr[0].contents}
       elif len(_fr)==0:
          return {'status': 'Error', 'message': 'file does not exist'}

    return {'status': 'Error', 'message': 'share id matched more than one file'}

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

      _files = FileRecord.query(FileRecord.user==self._user.key,
                               FileRecord.filename==_f.get_filename()).fetch()

      _md=_f.get_attribute('modified_date')
      if _md is None:
         _f.set_attribute('modified_date', 1)

      if len(_files)==1:
         _file=_files[0]
         #what to do if the file record already exists..
         _file.contents=_f.to_json()
         _file.modified_date=_f.get_attribute('modified_date')
         _file.put()
         return json.dumps({'status': 'Okay', 'message': 'File saved..'})

      if len(_files) == 0:
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

global_fs_id=0

class FileSystemNode:
  def __init__(self, name):
      global global_fs_id
      self._id=global_fs_id
      global_fs_id+=1

      self._isa_dir=False
      self._isa_file=False
      self._active=False
      self._shareid=None
      self._fullname=None

      self.name=name
      self.children=[]

  def get_child(self, name):
      for _child in self.children:
          if _child.name == name:
             return _child

      #if we get here, there is no child by that name
      _child=FileSystemNode(name)
      self.children.append(_child)
      return _child

  def get_dict(self, parentID=None):
      _dict={'name': self.name, 'id': self._id, 'unique_id': self._id,
             '_parentId': parentID, 'fullname': self._fullname, 'type': 'file'}
      if self._isa_dir:
         if parentID is None:
            _dict['state']='open'
         else:
            _dict['state']='closed'

         _dict['type']='dir'
         _dict['active']=self._active
         _dict['shareid']=self._shareid
         _dict['children']=[_d.get_dict(parentID=self._id) for _d in self.children]
      
      return _dict

class ShareHandler:
  def __init__(self, request):
      #assert isinstance(request, dict)
      self._request=request

      self._token=request.get('token', None)
      if isinstance(self._token, list):
         self._token=self._token[0]
      _results=User.query(User.token==self._token).fetch()
      if len(_results) == 1:
         self._user=_results[0]
      else:
         self._user=None

  def valid_token(self):
      if self._user is None:
         return False

      return self._user.expiration_date < datetime.datetime.fromtimestamp(time.time())

  def execute_command(self):
      _command=self._request.get('command', None)
      if isinstance(_command, list):
         _command=_command[0]

      if _command is None:
         return json.dumps({'status': 'Error', 'message': "invalid request"})

      if _command in ('filelist', 'listfiles'):
         return self.listfiles()
      elif _command in ('directory_access'):
         return self.directory_access()

      return json.dumps({'status': 'Error', 
                         'message': "invalid command '%s'" % _command})

  def listfiles(self):
      _fr=FileRecord.query(FileRecord.user==self._user.key).fetch()
      
      _dirs=[]
      _list=[]
      _root=FileSystemNode('/')
      _root._isa_dir=True

      for _f in _fr:
          #get dir
          _filename=_f.filename
          if _filename.startswith('/pyschool'):
             _filename=_filename[9:]

          if _filename.startswith('/'):
             _filename=_filename[1:]

          _parts=_filename.split('/')

          _dir=''
          _pos=_root
          for _part in _parts:
              _dir+='/%s' % _part
              _pos=_pos.get_child(_part)
              _pos._isa_dir=_part!=_parts[-1]
              _pos._isa_file=not _pos._isa_dir 
              #_pos.name=_dir
              _pos._fullname=_dir

              if _dir not in _dirs:
                 print _dir
                 _dirs.append(_dir)
                 _sr=ShareRecord.query(ShareRecord.dir == _dir,
                                       ShareRecord.user == self._user.key).fetch()
                 if len(_sr) == 1:
                    _sr[0]=_sr[0].key.get(use_cache=False)
                    _pos._shareid=_sr[0].shareid
                    _pos._active=_sr[0].active
                    #_pos.name=_dir
                    #_pos._fullname=_dir
                    _pos._isa_dir=_part != _parts[-1]
                    _pos._isa_file=not _pos._isa_dir
                 else:
                    print "list files ShareRecord", len(_sr)

      return json.dumps({'status': 'Okay', 'files': _root.get_dict()})

  def directory_access(self):
      _directories=self._request.get('directories', None)
      if _directories is None:
         return json.dumps({'status': 'Okay',
                            'message': 'Error! No directories to update'})
      
      _directories=json.loads(_directories[0])
      print _directories
      _count=0
      for _dir, _active in _directories.items():
          if not _dir.startswith('/'):
             _dir='/%s' % _dir

          print _dir
          _sr=ShareRecord.query(ShareRecord.dir==_dir, 
                                ShareRecord.user==self._user.key).fetch()

          if len(_sr) == 0:
             #this share does not exist.. so lets create it.
             _sr=ShareRecord()
             _sr.dir=_dir
             _sr.user=self._user.key
             _sr.shareid=hashlib.md5("%s:%s:%s" % (self._user, _dir, time.time())).hexdigest()
             _sr.active= _active in ('Y', u'Y')
             _sr.put()
             _count+=1
             print 'shareid0 %s "%s"' % ( _sr.shareid, _active)
             print _sr.is_saved
          elif len(_sr) == 1:
             _sr[0].user=self._user.key
             _sr[0].active= _active in ('Y', u'Y')
             if _sr[0].shareid in (None, '', ' '):
                _sr[0].shareid=hashlib.md5("%s:%s:%s" % (self._user, _dir, time.time())).hexdigest()
             _sr[0].put()
             _count+=1
             print 'shareid1 %s "%s"' % ( _sr[0].shareid, _sr[0].active)

             print _sr[0].is_saved
          else:
             #this shouldn't happen..
             #output an error
             print "len of ShareRecord is", len(_sr)

      return json.dumps({'status': 'Okay',
                         'message': 'Updated %d directories' % _count})
