## inspired by http://html5hub.com/build-a-javascript-particle-system/?utm_source=javascriptweekly&utm_medium=email

from browser import document, window, html
import math
import __random as random
from javascript import console

class Canvas:
  def __init__(self, id, parentID=None):
      self._id=id
     
      if parentID is not None:
          _parent=document[parentID]
          _canvas=html.CANVAS(id='canvas', style={'width': _parent.width, 'height':_parent.height, 'background-color': 'black'})
          _parent <= _canvas
         
      self._canvas = document[id]

  @property
  def ctx(self, type='2d'):
      return self._canvas.getContext(type)
     
  @property
  def width(self):
      return self._canvas.width

  @property
  def height(self):
      return self._canvas.height
         
  def clear(self, ctx):
      ctx.clearRect(0, 0, self._canvas.width, self._canvas.height)
     
     
  def loop(self, *args):
      _ctx = self.ctx
      self.clear(_ctx)
      self.update()
      self.draw()
      self.queue()

  def update(self):
      pass
 
  def draw(self):
      pass
 
  def queue(self):
      window.requestAnimationFrame(self.loop)

class ParticleCanvas(Canvas):
  def __init__(self, id, parentID, emitters, fields):
      Canvas.__init__(self, id, parentID)
      self._emitters=emitters
      self._fields=fields

  def update(self):
      for emitter in self._emitters:
          emitter.emitParticles()
         
      self.plotParticles()

  def draw(self):
      _ctx=self.ctx
      for emitter in self._emitters:
          emitter.draw(_ctx)
          for _particle in emitter._particles:
              _particle.draw(_ctx)

      for _field in self._fields:
          _field.draw(_ctx)

  def plotParticles(self):
      boundsX = self._canvas.width
      boundsY = self._canvas.height
     
      for emitter in self._emitters:
          for _particle in emitter._particles:
              pos = _particle._position
 
              #If we're out of bounds, drop this particle and move on to the next
              if boundsX < pos._x or boundsX < 0 or boundsY < pos._y or pos._y < 0:
                 emitter._particles.remove(_particle)
                 continue
 
              _particle.submitToFields(self._fields)
              #Move our particles
              # console.log(_particle._position._x, _particle._position._y)
              _particle.move()

class Vector:
  def __init__(self, x=0, y=0):
      self._x=x
      self._y=y
     
  def __add__(self, other):
      self._x+=other._x
      self._y+=other._y
      return self
     
  def __sub__(self, other):
      self._x-=other._x
      self._y-=other._y
      return self
     
  def getMagnitude(self):
      return self._x * self._x + self._y * self._y
     
  def getAngle(self):
      return math.atan2(self._y,self._x)
     
def fromAngle(angle, magnitude):
  return Vector(x=magnitude * math.cos(angle), y=magnitude * math.sin(angle))
     
class Particle:
  def __init__(self, position = Vector(0,0), velocity=Vector(0,0), acceleration=Vector(0,0)):
      self._position=position
      self._velocity=velocity
      self._acceleration=acceleration
      self._size=1

  def move(self):
      #Add our current acceleration to our current velocity
      self._velocity += self._acceleration
 
      #Add our current velocity to our position
      self._position += self._velocity

  def draw(self, ctx):
      #Set the color of our particles
      ctx.fillStyle = 'rgb(0,0,255)'
 
      #Draw a square at our position [particleSize] wide and tall
      ctx.fillRect(self._position._x, self._position._y, self._size, self._size)

  def submitToFields(self, fields):
      #our starting acceleration this frame
      totalAccelerationX = 0
      totalAccelerationY = 0
 
      #for each passed field
      for _field in fields:
          _vectorX = _field._position._x - self._position._x
          _vectorY = _field._position._y - self._position._y
 
          #calculate the force via MAGIC and HIGH SCHOOL SCIENCE!
          _div=math.pow(_vectorX*_vectorX+_vectorY*_vectorY,1.5)
          if _div == 0:
              _force=0
          else:
             _force = _field._mass / _div
        
          #add to the total acceleration the force adjusted by distance
          totalAccelerationX += _vectorX * _force
          totalAccelerationY += _vectorY * _force
 
      #update our particle's acceleration
      self._acceleration = Vector(totalAccelerationX, totalAccelerationY)


class Emitter:
  def __init__(self, point, velocity, spread=math.pi/32):
      self._position=point
      self._velocity=velocity
      self._spread=spread
      self._drawColor="#999"
      self._particles=[]
       
  def emitParticle(self):
      #Use an angle randomized over the spread so we have more of a "spray"
      angle = self._velocity.getAngle() + self._spread - (random.random() * self._spread * 2)
 
      #The magnitude of the emitter's velocity
      magnitude = self._velocity.getMagnitude()
 
      #The emitter's position
      _position = Vector(self._position._x, self._position._y)
 
      #New velocity based off of the calculated angle and magnitude
      _velocity = fromAngle(angle, magnitude)
     
      #return our new Particle!
      return Particle(position=_position, velocity=_velocity)
 
  def emitParticles(self, maxParticles=200, emissionRate=2):
      if len(self._particles) > maxParticles:
          return
     
      for _i in range(emissionRate):
          self._particles.append(self.emitParticle())

  def draw(self, ctx):
      size=4
      ctx.fillStyle = self._drawColor
      ctx.beginPath()
      ctx.arc(self._position._x, self._position._y, size, 0, math.pi * 2)
      ctx.closePath()
      ctx.fill()

class Field:
  def __init__(self, position, mass=100):
      self._position=position
      self._mass=mass
      if mass < 0:
         self._drawColor = "#f00"
      else:
         self._drawColor = "#0f0"
         
     
  def draw(self, ctx):
      size=4
      ctx.fillStyle = self._drawColor
      ctx.beginPath()
      ctx.arc(self._position._x, self._position._y, size, 0, math.pi * 2)
      ctx.closePath()
      ctx.fill()


#_width=document['pydiv'].width
#_height=document['pydiv'].height
emitters=[Emitter(Vector(100, 100), fromAngle(0,2))]
fields = [Field(Vector(200, 100), -140)]
pc=ParticleCanvas('canvas', 'pydiv', emitters=emitters, fields=fields)
pc.loop()
