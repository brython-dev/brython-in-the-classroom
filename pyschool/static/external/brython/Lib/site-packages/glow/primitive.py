from javascript import JSConstructor, JSObject
from .vector import vec

class primitive:
  def __init__(self, prim, **kwargs):
      for _key in kwargs.keys():
          if isinstance(kwargs[_key], vec):
             kwargs[_key]=kwargs[_key]._vec

      self._prim=prim(kwargs)

  def rotate(self, **kwargs):
      if 'axis' in kwargs:
         #for now lets assume axis is a vector
         kwargs['axis']=kwargs['axis']._vec

      self._prim.rotate(kwargs)

  @property
  def pos(self):
      _v=vec()
      _v._set_vec(self._prim.pos)
      return _v

  @pos.setter
  def pos(self, value):
      if isinstance(value, vec):
         self._prim.pos=value._vec
      else:
         print("Error! pos must be a vector")

  @property
  def color(self):
      _v=vec()
      _v._set_vec(self._prim.color)
      return _v

  @color.setter
  def color(self, value):
      if isinstance(value, vec):
         self._prim.color=value._vec
      else:
         print("Error! color must be a vec")

  @property
  def axis(self):
      _v=vec()
      _v._set_vec(self._prim.axis)
      return _v

  @axis.setter
  def axis(self, value):
      if isinstance(value, vec):
         self._prim.axis=value._vec
      else:
         print("Error! axis must be a vec")

  @property
  def size(self):
      return self._prim.size

  @size.setter
  def size(self, value):
      self._prim.size=value

  @property
  def up(self):
      _v=vec()
      _v._set_vec(self._prim.up)
      return _v

  @up.setter
  def up(self, value):
      if isinstance(value, vec):
         self._prim.up=value._vec
      else:
         print("Error! up must be a vec")

  @property
  def opacity(self):
      return self._prim.opacity

  @opacity.setter
  def opacity(self, value):
      self._prim.opacity=value

  @property
  def shininess(self):
      return self._prim.shininess

  @shininess.setter
  def shininess(self, value):
      self._prim.shininess=value

  @property
  def emissive(self):
      return self._prim.emissive

  @emissive.setter
  def emissive(self, value):
      self._prim.emissive=value

  @property
  def texture(self):
      return self._prim.texture

  @texture.setter
  def texture(self, **kwargs):
      self._prim.texture=kwargs

  @property
  def visible(self):
      return self._prim.visible

  @visible.setter
  def visible(self, flag):
      assert isinstance(flag, bool)

      self._prim.visble=flag

class arrow(primitive):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.arrow), **kwargs)

class box(primitive):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.box), **kwargs)

class cone(primitive):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.cone), **kwargs)

class curve(primitive):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.curve), **kwargs)

  def push(self, v):
      if isinstance(v, vec):
         self._prim.push(v._vec)
      elif isinstance(v, dict):
         for _key in v.keys():
             if isinstance(_key, vec):
                v[_key]=v[_key]._vec

         self._prim.push(v)

  def append(self, v):
      self.push(v)

class cylinder(primitive):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.cylinder), **kwargs)

class helix(cylinder):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.helix), **kwargs)

class pyramid(primitive):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.pyramid), **kwargs)

#class ring(curve):

class sphere(primitive):
  def __init__(self, **kwargs):
      primitive.__init__(self, JSConstructor(glowscript.sphere), **kwargs)


#triangle
#class triangle:
#  def __init__(self, **kwargs):
#      self._tri = JSConstructor(glowscript.triangle)(kwargs)

#vertex
#class vertex:
#  def __init__(self, **kwargs):
#      self._ver = JSConstructor(glowscript.vertex)(kwargs)


#quad

#compound
#class compound(box):
#  def __init__(self, **kwargs):
#      box.__init__(self, kwargs)

# I'm not sure if the declarations below are correct.  Will fix later.

class distinct_light:
  def __init__(self, **kwargs):
      self._dl=JSConstructor(glowscript.distant_light)(kwargs)

class local_light:
  def __init__(self, **kwargs):
      self._ll=JSConstructor(glowscript.local_light)(kwargs)

class draw:
  def __init__(self, **kwargs):
      self._draw=JSConstructor(glowscript.draw)(kwargs)

class label:
  def __init__(self, **kwargs):
      self._label=JSConstructor(glowscript.label)(kwargs)

def attach_trail(object, **kwargs):
    if isinstance(object, primitive):
       JSObject(glowscript.attach_trail)(object._prim, kwargs)
    else:
       JSObject(glowscript.attach_trail)(object, kwargs)

