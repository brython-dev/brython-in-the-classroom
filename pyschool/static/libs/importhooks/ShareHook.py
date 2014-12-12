import BaseHook

import urllib
import sys

sys.path.append("../FileSystem")
import FileObject

#define my custom import hook (just to see if it get called etc).
class ShareHook(BaseHook.BaseHook):
  def __init__(self, fullname, path):
      BaseHook.BaseHook.__init__(self, fullname, path)
      if '/Shares/' not in path:
         raise ImportError

      #self._fullname=fullname
      #self._path=path    # we don't are about this...

      if path.endswith('/'):
         path=path[:-1]

      if not fullname.startswith('/'):
         fullname='/%s' % fullname

      self._modpath="%s%s.py" % (path, fullname)

  def find_module(self):
      _fp,_,_=urllib.request.urlopen(self._modpath)
      #try:
      _data=_fp.read()

      _msg=json.loads(_data)
      if _msg['status'] != 'Okay':
         raise ImportError

      _fileobj=FileObject.FileObject()
      _fileobj.from_json(_msg['fileobj'])
      self._module=_fileobj.get_attribute('contents')

      return self

sys.meta_path.append(ShareHook)
