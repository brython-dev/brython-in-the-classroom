from browser.local_storage import storage
import FileSystemBase

from javascript import console

class FileSystem(FileSystemBase.FileSystem):
  def __init__(self, root):
      FileSystemBase.FileSystem.__init__(self, root)

  def _list_files(self):
      """ returns a list of files this person has on storage,
          return empty list [] if unsuccessful
      """
      try:
        return storage.keys()
      except:
        pass

      return []

  def _read_file(self, filename):
      """ retrieves file from storage, returns fileobj if successful,
          return None if unsuccessful
      """
      try:
        _json=storage[filename]
      except KeyError:
        return None

      _f=FileSystemBase.FileObject()
      _f.from_json(_json)
      return _f

  def _write_file(self, fileobj):
      """saves a file to storage, returns True if save was successful,
         False, if unsuccessful
      """
   
      try:
         storage[fileobj.get_attribute('filename')] = fileobj.to_json()
      except:
         return False

      return True      
      

  def _rm_file(self, filename):
      """removes a file in storage, returns True if delete was successful,
         False, if unsuccessfull
      """
      try:
         del storage[filename]
      except KeyError:
         return None

      return True
