import json
from javascript import console
import FileObject
#from .FileObject import FileObject
#from . import FileObject

import datetime

unique_id=0

class FileSystemNode:
  def __init__(self, name):
      global unique_id
      self.unique_id=unique_id
      unique_id+=1
      self._isa_dir=False
      self._isa_file=False
      self.children=[]
      self.name=name
      self.modified_date='1900-01-01'
      self.fullname=None

  def isa_dir(self):
      return self._isa_dir

  def children(self):
      return self.children

  def get_child(self, name):
      for _child in self.children:
          if _child.name == name:
             return _child

      #if we get here, there is no child by that name
      _child=FileSystemNode(name)
      self.children.append(_child)
      return _child

class FileSystem:
  def __init__(self, root='/'):
      self._root=root

  def _prefix_check(self, name):
      if name.startswith(self._root):
         return name

      if name.startswith('/'):
         name=name[1:]

      return "%s/%s" % (self._root, name)

  def _list_files(self):
      """ returns a list of files this person has on storage,
          return None if unsuccessful
      """
      pass

  def _read_file(self, filename):
      """ retrieves file from storage, returns fileobj if successful,
          return None if unsuccessful
      """
      pass

  def _write_file(self, fileobj):
      """saves a file to storage, returns True if save was successful,
         False, if unsuccessfull
      """
      pass

  def _rm_file(self, filename):
      """removes a file in storage, returns True if delete was successful,
         False, if unsuccessfull
      """
      pass

  def _modified_date(self, filename):
      """ returns a file's last modification date,
          for some implementations, this could be an expensive operation
          if so, just return a date such as '1900-01-01'
      """
      return 1

  def listdir(self, directory, callback):
      directory=self._prefix_check(directory)

      #_filenames=self._list_files()
      _results=self._list_files()
      if _results['status'] == 'Error':
         _results['filelist']=[]
         callback(_results)
         return

      _root=FileSystemNode(name='/')
      _root._isa_dir=True

      _files=_results['filelist']
      #console.log(_files)
      for _file in _files:
          _fullname=_file['filename']
          if _fullname.startswith(directory):
             _filename=_fullname[len(directory):]
             _dirs=_filename.split('/')

             _pos=_root
             for _dir in _dirs:
                 _pos=_pos.get_child(_dir)
                 _pos._isa_dir=_dir != _dirs[-1]
                 _pos._isa_file=not _pos._isa_dir

                 if _pos._isa_file:
                    _pos.fullname=_fullname
                    _tstamp=_file.get('modified_date',
                                      self._modified_date(_fullname))
                    if not isinstance(_tstamp, (int,)):
                       _tstamp=1
                    #console.log(_tstamp)
                    _md=datetime.datetime.fromtimestamp(_tstamp)
                    #console.log(str(_md))
                    _pos.modified_date=str(_md)
      
      callback({'status': 'Okay', 'filelist': _root})

  def read_file(self, filename, callback):
      filename=self._prefix_check(filename)
      callback(self._read_file(filename))

  def save_file(self, fileobj, callback):
      assert isinstance(fileobj, FileObject.FileObject)
      #assert isinstance(fileobj, FileObject)

      _filename=fileobj.get_filename()
      assert _filename is not None

      _filename=self._prefix_check(_filename)
      fileobj.set_filename(_filename) #the name may have changed
      #fix me  brython issue  _time.mktime
      #fileobj.set_attribute('modified_date', int(datetime.datetime.now().timestamp()))
      fileobj.set_attribute('modified_date', 1412391232)
      callback(self._write_file(fileobj))

  def rm_file(self, filename, callback):
      filename=self._prefix_check(filename)
      callback(self._rm_file(filename))
