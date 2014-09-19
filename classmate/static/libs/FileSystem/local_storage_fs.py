import FileObject
from browser.local_storage import storage

class FileSystem:
  def __init__(self, root='/'):
      self._root=root
      self._cwd=root

  #def getcwd(self):
  #    return self._cwd

  #def mkdir(self, dir):
  #    #this really doesn't do anything
  #    pass

  def listdir(self, directory):
      _results=[]
      for _filename in storage.keys():
          if _filename.startswith(directory):
             _file=_filename[len(directory)+1:]
             _basename, _dummy=_file.split('/',1)
             _results.append(_basename)

      _results.sort()

      return _results

  def read_file(self, filename):
      return storage.getdefault(filename, None)

  def save_file(self, fileobj):
      assert isinstance(fileobj, FileObject.FileObject)
      assert fileobj.get_attribute('filename') is not None

      storage[fileobj.get_attribute('filename')]=fileobj.to_json()

  def rm_file(self, filename):
      if filename in storage.keys():
         del storage[filename]
         return

      #todo:should raise some type of error..
