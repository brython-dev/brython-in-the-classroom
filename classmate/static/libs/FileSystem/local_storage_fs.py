import FileObject
from browser.local_storage import storage
from javascript import console

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

  def listdir(self, directory, callback):
      directory=self._prefix_check(directory)

      _root=FileSystemNode(name='/')
      _root._isa_dir=True

      for _filename in storage.keys():
          if _filename.startswith(directory):
             console.log(_filename)
             _file=_filename[len(directory):]
             _dirs=_file.split('/')

             _pos=_root
             for _dir in _dirs:
                 _pos=_pos.get_child(_dir)
                 _pos._isa_dir=_dir != _dirs[-1]
                 _pos._isa_file=not _pos._isa_dir

                 if _pos._isa_file:
                    _pos.fullname=_filename
      
      callback(_root)

  def read_file(self, filename, callback):
      filename=self._prefix_check(filename)
      try:
         _json=storage[filename]
      except KeyError:
         callback(None)
         return

      _f=FileObject.FileObject()
      _f.from_json(_json)
      callback(_f)

  def save_file(self, fileobj, callback):
      assert isinstance(fileobj, FileObject.FileObject)

      _filename=fileobj.get_attribute('filename')
      assert _filename is not None

      _filename=self._prefix_check(_filename)

      storage[_filename]=fileobj.to_json()
      callback(True)

  def rm_file(self, filename, callback):
      filename=self._prefix_check(filename)

      try:
        del storage[filename]
        callback(True)
      except:
        pass
        #todo:should raise some type of error..
