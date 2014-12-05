import os
import json

_dict={}

for _root, _dirs, _files in os.walk('FileSystem'):
    for _file in _files:
        if _file.endswith('.py'):
           _fp=open(os.path.join(_root, _file), 'r')
           _data=_fp.read()
           _fp.close()

           _dict[_file.replace('.py', '')]=_data

_fp=open('custom_VFS.js', 'w')
_fp.write("window._custom_VFS=%s" % json.dumps(_dict))
_fp.close()
