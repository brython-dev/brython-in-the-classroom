from javascript import JSObject
import sys

#define my custom import hook (just to see if it get called etc).
class CustomVFS:
  def __init__(self, fullname, path):
      self._fullname=fullname
      self._path=path    # we don't are about this...

      self._modules=dict(JSObject(window._custom_VFS))

  def find_module(self):
      if '%s.py' % (self._fullname) not in self._modules:
         raise ImportError

      return self
      
  def load_module(self, name):
      return self._modules['%s.py' % self._fullname]

# we probably want to add this to sys.meta_path, so lets just do it for the
# user

sys.meta_path.append(CustomVFS)
