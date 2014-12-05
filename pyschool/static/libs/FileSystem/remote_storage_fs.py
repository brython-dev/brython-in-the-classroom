from browser.local_storage import storage
import FileSystemBase
import FileObject

import urllib.request
import json
from javascript import console

class RemoteFileSystem(FileSystemBase.FileSystem):
  def __init__(self, root, baseURL, token=None):
      FileSystemBase.FileSystem.__init__(self, root)
      self._baseURL=baseURL
      self._token=token

  def set_token(self, token):
      self._token=token

  def _remote_call(self, data):
      #console.log("remote call", data)
      data['token']=self._token   #add in token to call
      _json=json.dumps({'data': data})

      try:
        _fp,_url,_headers=urllib.request.urlopen(self._baseURL, _json)
        return json.loads(_fp.read())   #returns a string (in json format)
      except:
        return {'status': 'Error', 
                'message': 'Network connectivity issues'}

  def _list_files(self):
      """ returns a list of files this person has on storage,
          return empty list [] if unsuccessful
      """

      #return json.loads(self._remote_call({'command': 'list_files', 'directory': '/'}))
      return self._remote_call({'command': 'list_files', 'directory': '/'})

  def _read_file(self, filename):
      """ retrieves file from storage, returns fileobj if successful,
          return None if unsuccessful
      """
      
      _json=self._remote_call({'command': 'read_file', 'filename': filename})

      try:
        _f=FileObject.FileObject()
        #_f=FileSystemBase.FileObject()
        _f.from_json(_json['fileobj'])
        return {'status': 'Okay', 'fileobj': _f}
      except Exception as e:
        return {'status': 'Error', 'message': str(e)}

  def _write_file(self, fileobj):
      """saves a file to storage, returns True if save was successful,
         False, if unsuccessful
      """
   
      _fileobj=fileobj.to_json()
      _res=self._remote_call({'command': 'write_file', 'fileobj': _fileobj})
      return _res
      

  def _rm_file(self, filename):
      """removes a file in storage, returns True if delete was successful,
         False, if unsuccessfull
      """

      _res=self._remote_call({'command': 'rm_file', 'filename': filename})
      return _res


class GoogleDataStorage(RemoteFileSystem):
  def __init__(self, root):
      RemoteFileSystem.__init__(self, root, "/FS")
