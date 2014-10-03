import json

class CommandHandler:
  def __init__(self, request):
      assert isinstance(request, dict)
      self._request=request

  def execute_command(self):
      _command=self._request.get('command', None)

      if _command is None:
         return "invalid request"

      if _command == 'list_files':
         return self.list_files()
      elif _command == 'read_file':
         return self.read_file()
      elif _command == 'write_file':
         return self.write_file()
      elif _command == 'rm_file':
         return self.rm_file()

      return "invalid command"

  def list_files(self):
      _dir=self._request.get('directory', '/')

      #retrieve a list of files this person has access to.
      return json.dumps(self._list_files(_dir))

  def read_file(self):
      _filename=self._request['filename']
      return self._read_file(_filename)

  def write_file(self):
      _fileobj=self._request['fileobj']  #already a json string!
      if self._write_file(_fileobj):
         return json.dumps({'status': 'Okay', 'message': 'File saved successfully!'})

      #something went wrong...
      return json.dumps({'status': 'Error', 'message': 'File not saved..'})
      

  def rm_file(self):
      _filename=self._request['filename']
      return self._rm_file(_filename)

  def _list_files(self, directory):
      pass

  def _read_file(self, filename):
      pass

  def _write_file(self, filename, contents):
      pass

  def _rm_file(self, filename):
      pass
