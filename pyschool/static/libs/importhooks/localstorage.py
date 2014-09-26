from browser.local_storage import storage
import sys

#define my custom import hook (just to see if it get called etc).
class LocalStorageHook:
  def __init__(self, fullname, path):
      self._fullname=fullname
      self._path=path

  def find_module(self):
      for _ext in ('.py', '/__init__.py'):
          try:
             _modpath='%s/%s%s' % (self._path, self._fullname, _ext)
             print('search path: %s' % _modpath)
             self._module=storage[_modpath]
             return self
          except:
             pass
    
      #if we got here, we couldn't find the module
      raise ImportError
      
  def load_module(self, name):
      return self._module

# we probably want to add this to sys.meta_path, so lets just do it for the
# user

sys.meta_path.append(LocalStorageHook)
