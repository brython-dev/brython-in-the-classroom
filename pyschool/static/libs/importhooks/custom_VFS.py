from browser import window
from javascript import JSObject
import sys

_modules=dict(JSObject(window._custom_VFS))

class TempMod:
  def __init__(self, name):
      self.name=name

#define my custom import hook (just to see if it get called etc).
class CustomVFS:
  def __init__(self, fullname, path):
      self._fullname=fullname
      self._path=path    # we don't are about this...
      self._modpath='CUSTOM VFS'

  def find_module(self):
      self._module=_modules.get(self._fullname, None)
      if self._module is None:
         raise ImportError

      return self

  def load_module(self, name):
      _mod=JSObject(__BRYTHON__.run_py)(TempMod(self._fullname),
                                        self._modpath, self._module)
      _mod.is_package='.' in self._fullname
      return _mod

# we probably want to add this to sys.meta_path, so lets just do it for the
# user

sys.meta_path.append(CustomVFS)
