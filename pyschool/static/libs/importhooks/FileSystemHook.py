from browser import window
from javascript import console, JSObject

import sys
sys.path.append("../FileSystem")

import FileObject

#define my custom import hook (just to see if it get called etc).
class FileSystemHook:
  def __init__(self, fullname, path):
      self._fullname=fullname
      self._path=path

      if not path.startswith('/pyschool'):
         raise ImportError

  def find_module(self):
      def cb(value):
          pass

      if not self._path.startswith('/pyschool'):
         raise ImportError

      fs=JSObject(window._FS)
      console.log(fs.__name__)

      for _ext in ('.py', '/__init__.py'):
          _modpath='%s/%s%s' % (self._path, self._fullname, _ext)
          _msg=fs._read_file(_modpath)

          if _msg['status'] == 'Okay':
             self._module=_msg['fileobj'].get_attribute('contents')
             return self
    
      #if we got here, we couldn't find the module
      raise ImportError
      
  def load_module(self, name):
      return self._module

# we probably want to add this to sys.meta_path, so lets just do it for the
# user

sys.meta_path.append(FileSystemHook)
