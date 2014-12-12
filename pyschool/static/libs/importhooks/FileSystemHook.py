import BaseHook
from browser import window
from javascript import JSObject

import sys
sys.path.append("../FileSystem")

import FileObject

#define my custom import hook (just to see if it get called etc).
class FileSystemHook(BaseHook.BaseHook):
  def __init__(self, fullname, path):
      BaseHook.BaseHook.__init__(self, fullname, path)

      if not path.startswith('/pyschool'):
         raise ImportError

  def find_module(self):
      if not self._path.startswith('/pyschool'):
         raise ImportError

      fs=JSObject(window._FS)

      for _ext in ('.py', '/__init__.py'):
          self._modpath='%s/%s%s' % (self._path, self._fullname, _ext)
          _msg=fs._read_file(self._modpath)

          if _msg['status'] == 'Okay':
             self._module=_msg['fileobj'].get_attribute('contents')
             return self
    
      #if we got here, we couldn't find the module
      raise ImportError

sys.meta_path.append(FileSystemHook)
