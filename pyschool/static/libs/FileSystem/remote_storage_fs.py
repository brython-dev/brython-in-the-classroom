from browser.local_storage import storage
import FileSystemBase

import urllib.request
import json
from javascript import console

class RemoteFileSystem(FileSystemBase.FileSystem):
  def __init__(self, root, baseURL, token):
      FileSystemBase.FileSystem.__init__(self, root)
      self._baseURL=baseURL
      self._token=token

  def _remote_call(self, data):
      data['token']=self._token   #add in token to call
      _json=json.dumps({'json': data})
      _fp,_url,_headers=urllib.request(self._baseURL, data=_json, 5)
      _data=_fp.read()
      return json.loads(_data)


  def _list_files(self):
      """ returns a list of files this person has on storage,
          return empty list [] if unsuccessful
      """

      try:
         return self._remote_call({'command': 'list_files', 'directory': '/'})
      except:
        pass

      return []

  def _read_file(self, filename):
      """ retrieves file from storage, returns fileobj if successful,
          return None if unsuccessful
      """
      try:
         _json=self._remote_call({'command': 'read_file', 'filename': filename})
      except KeyError:
        return None

      _f=FileObject.FileObject()
      _f.from_json(_json)
      return _f

  def _write_file(self, fileobj):
      """saves a file to storage, returns True if save was successful,
         False, if unsuccessful
      """
   
      _fileobj=fileobj.to_json()
      try:
         _json=self._remote_call({'command': 'write_file', 'fileobj': _fileobj})
      except:
         return False

      return True      
      

  def _rm_file(self, filename):
      """removes a file in storage, returns True if delete was successful,
         False, if unsuccessfull
      """
      try:
         _json=self._remote_call({'command': 'rm_file', 'filename': filename})
      except:
         return None

      return True
