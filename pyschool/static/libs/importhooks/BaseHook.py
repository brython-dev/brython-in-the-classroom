from javascript import JSObject

class TempMod:
  def __init__(self, name):
      self.name=name

#define my custom import hook (just to see if it get called etc).
class BaseHook:
  def __init__(self, fullname, path):
      self._fullname=fullname
      self._path=path    # we don't are about this...
      self._modpath=''
      self._module=''

  def is_package(self):
      return '.' in self._fullname

  def load_module(self, name):
      return JSObject(__BRYTHON__.run_py)(TempMod(self._fullname),
                                        self._modpath, self._module)
