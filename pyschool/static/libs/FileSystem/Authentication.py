class Authentication:
  def __init__(self, userid, password):
      self._userid=userid
      self._password=password

      self._token=None

  def get_token(self):
      return self._token

  def set_token(self, token):
      self._token=token
