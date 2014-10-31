import urllib
import sys

sys.path.append("../FileSystem")
import FileObject

#define my custom import hook (just to see if it get called etc).
class ShareHook:
  def __init__(self, fullname, path):
      if '/Shares/' not in path:
         raise ImportError

      self._fullname=fullname
      self._path=path    # we don't are about this...

      if path.endswith('/'):
         path=path[:-1]

      if not fullname.startswith('/'):
         fullname='/%s' % fullname

      self._url="%s%s.py" % (path, fullname)
      print(self._url)
      #"/Shares?shareid=%s/%s.py" % (path[7:], fullname.replace('.', '/'))

  def find_module(self):
      _fp,_,_=urllib.request.urlopen(self._url)
      #try:
      _data=_fp.read()
      print(_data)
      _msg=json.loads(_data)
      if _msg['status'] != 'Okay':
         raise ImportError

      _fileobj=FileObject.FileObject()
      _fileobj.from_json(_msg['fileobj'])
      self._module=_fileobj.get_attribute('contents')
      print(self._module)
      #except:
      #  raise ImportError

      return self
      
  def load_module(self, name):
      return self._module

# we probably want to add this to sys.meta_path, so lets just do it for the
# user

sys.meta_path.append(ShareHook)
