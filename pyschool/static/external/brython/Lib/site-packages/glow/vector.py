from javascript import JSConstructor, console

class vec:
  def __init__(self, x=0, y=0, z=0):
      self._vec=JSConstructor(glowscript.vec)(x,y,z)

      self.add=self.__add__
      self.sub=self.__sub__
      self.multiply=self.__mul__
      self.divide=self.__truediv__=self.__div__

  #vec should be a glowscript vec, not an instance of this class
  def _set_vec(self, vec):
      self._vec=vec

  @property
  def x(self):
      return self._vec.x

  @x.setter
  def x(self, value):
      self._vec.x=value

  @property
  def y(self):
      return self._vec.y

  @y.setter
  def y(self, value):
      self._vec.y=value

  @property
  def z(self):
      return self._vec.z

  @z.setter
  def z(self, value):
      self._vec.z=value

  def __add__(self, other):
      if isinstance(other, vec):
         _v=vec()
         _v._set_vec(self._vec.add(other._vec))
         return _v

      raise ImplementationError("addition of vec and %s not implemented yet"  % type(other))

  def __sub__(self, other):
      if isinstance(other, vec):
         _v=vec()
         _v._set_vec(self._vec.sub(other._vec))
         return _v

      raise ImplementationError("subtraction of vec and %s not is implemented yet"  % type(other))


  def __mul__(self, other):
      if isinstance(other, int) or isinstance(other, float):
         _v=vec()
         _v._set_vec(self._vec.multiply(other))
         return _v

      raise ImplementationError("multiplication of vec and %s is not implemented yet"  % type(other))

  def __div__(self, other):
      if isinstance(other, int) or isinstance(other, float):
         _v=vec()
         _v._set_vec(self._vec.divide(other))
         return _v

      raise ImplementationError("division of vec and %s is not implemented yet"  % type(other))

  def __eq__(self, other):
      return self._vec.equals(other._vec)

  def __repr__(self):
      return self._vec.toString()

  def __str__(self):
      return self._vec.toString()

  def comp(self, other):
      return self._vec.comp(other._vec)

  def cross(self, other):
      return self._vec.cross(other._vec)

  def diff_angle(self, other):
      return self._vec.diff_angle(other._vec)

  def dot(self):
      return self._vec.dot()

  def mag(self):
      return self._vec.mag()

  def mag2(self):
      return self._vec.mag2()

  def norm(self):
      _v=vec()
      _v._set_vec(self._vec.norm())
      return _v

  def proj(self, other):
      _v=vec()
      _v._set_vec(self._vec.proj(other._vec))
      return _v

  def random(self):
      _v = vec()
      _v._set_vec(self._vec.random())
      return _v

  def rotate(self, **kwargs):
      _v = vec()
      _v._set_vec(self._vec.rotate(kwargs))
      return _v

  def to_glowscript(self):
      return self._vec
