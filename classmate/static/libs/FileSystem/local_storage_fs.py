import FileObject
from browser.local_storage import storage
from javascript import console

class FileSystem:
  def __init__(self, root='/'):
      self._root=root

  def listdir(self, directory, callback):
      _results=[]
      for _filename in storage.keys():
          if _filename.startswith(directory):
             _file=_filename[len(directory)+1:]
             _basename, _dummy=_file.split('/',1)
             _results.append(_basename)

      _results.sort()

      callback(_results)

  def read_file(self, filename, callback):
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
      assert fileobj.get_attribute('filename') is not None

      storage[fileobj.get_attribute('filename')]=fileobj.to_json()
      callback(True)

  def rm_file(self, filename, callback):
      try:
        del storage[filename]
        callback(True)
      except:
        pass
        #todo:should raise some type of error..
