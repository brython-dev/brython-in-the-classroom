from browser import window
from javascript import JSObject
import sys

_modules=dict(JSObject(window._custom_VFS))

#define my custom import hook (just to see if it get called etc).
class CustomVFS:
  def __init__(self, fullname, path):
      #console.log(fullname)
      self._fullname=fullname
      self._path=path    # we don't are about this...

  def find_module(self):
      _mod=_modules.get(self._fullname, None)
      if _mod is None:
         raise ImportError

      self._module=_mod

      return self
      
  def load_module(self, name):
      return self._module

# we probably want to add this to sys.meta_path, so lets just do it for the
# user

sys.meta_path.append(CustomVFS)
