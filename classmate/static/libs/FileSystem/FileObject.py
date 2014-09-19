import json

class FileObject:
  def __init__(self):
      self._dict={}

  def get_attribute(self, name):
      return self._dict.getdefault(name, None)

  def set_attribute(self, name, value):
      self._dict[name]=value

  def to_json(self):
      return json.dumps(self._dict)

  def from_json(self, json_string):
      self._dict=json.loads(json_string)
