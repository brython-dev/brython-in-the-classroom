import json

class FileObject:
  def __init__(self, metadata={}):
      assert isinstance(metadata, dict), "metadata must be a dictionary"
      self._metadata=metadata

  def get_attribute(self, name):
      return self._metadata.get(name, None)

  def set_attribute(self, name, value):
      self._metadata[name]=value

  def to_json(self):
      return json.dumps(self._metadata)

  def from_json(self, json_string):
      self._metadata=json.loads(json_string)

  def get_filename(self):
      return self._metadata['filename']

  def set_filename(self, filename):
      self._metadata['filename']=filename
