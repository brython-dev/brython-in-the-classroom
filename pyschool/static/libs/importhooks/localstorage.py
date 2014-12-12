import BaseHook
from browser.local_storage import storage
import sys

#define my custom import hook (just to see if it get called etc).
class LocalStorageHook(BaseHook.BaseHook):
  def __init__(self, fullname, path):
      BaseHook.BaseHook.__init__(self, fullname, path)
      #self._fullname=fullname
      #self._path=path
      #self._modpath=None

  def find_module(self):
      for _ext in ('.py', '/__init__.py'):
          try:
             self._modpath='%s/%s%s' % (self._path, self._fullname, _ext)
             self._module=storage[self._modpath]
             return self
          except:
             pass
    
      #if we got here, we couldn't find the module
      raise ImportError

sys.meta_path.append(LocalStorageHook)
