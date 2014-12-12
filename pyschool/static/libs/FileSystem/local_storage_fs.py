from browser.local_storage import storage
import FileSystemBase
import FileObject

import json
from javascript import console

class FileSystem(FileSystemBase.FileSystem):
  def __init__(self, root):
      FileSystemBase.FileSystem.__init__(self, root)

  def _list_files(self):
      """ returns a list of files this person has on storage,
          return empty list [] if unsuccessful
      """

      _list=[]
      for _file in storage.keys():
          if not _file.startswith('/pyschool'): continue
          try:
            _fileobj=FileObject.FileObject()
            #_fileobj=FileSystemBase.FileObject()
            _fileobj.from_json(storage[_file])
          except Exception as e:
            #not a FileObject file..
            console.log(str(e))
            console.log('not a fileobject...', _file)
            continue

          _list.append({'filename': _fileobj.get_filename(), 
                        'modified_date': _fileobj.get_attribute('modified_date')})

      return {'status': 'Okay', 'filelist': _list}

  def _read_file(self, filename):
      """ retrieves file from storage, returns fileobj if successful,
          return None if unsuccessful
      """
      try:
        _json=storage[filename]
      except KeyError:
        return {'status': 'Error', 'message': 'File doesn''t exist'}

      _f=FileObject.FileObject()
      #_f=FileSystemBase.FileObject()
      _f.from_json(_json)
      return {'status': 'Okay', 'fileobj': _f}

  def _write_file(self, fileobj):
      """saves a file to storage, returns True if save was successful,
         False, if unsuccessful
      """
   
      try:
         storage[fileobj.get_attribute('filename')] = fileobj.to_json()
      except Exception as e:
         return {'status': 'Error', 'message': str(e)}

      return {'status': 'Okay', 'message': 'File Saved...'}
      

  def _rm_file(self, filename):
      """removes a file in storage, returns True if delete was successful,
         False, if unsuccessfull
      """
      try:
         del storage[filename]
      except Exception as e:
         return {'status': 'Error', 'message': str(e)}

      return {'status': 'Okay', 'message': 'File Removed...'}
