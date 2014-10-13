from glow import *

glow('pydiv')
scene = canvas()

side = 4.0
thk = 0.3
s2 = 2*side - thk
s3 = 2*side + thk
wallR = box (pos=vec( side, 0, 0), size=vec(thk,s2,s3),  color=color.red)
wallL = box (pos=vec(-side, 0, 0), size=vec(thk,s2,s3),  color=color.red)
wallB = box (pos=vec(0, -side, 0), size=vec(s3,thk,s3),  color=color.blue)
wallT = box (pos=vec(0,  side, 0), size=vec(s3,thk,s3),  color=color.blue)
wallBK = box(pos=vec(0, 0, -side), size=vec(s2,s2,thk), color=color.gray(0.7))

ball = sphere(color=color.green, size=vec(0.8,0.8,0.8))
ball.mass = 1.0
ball.p = vec(-0.15, -0.23, +0.27)
#attach_trail(ball, pps=200, retain=100)

side = side - thk*0.5 - ball.size.x/2
dt = 0.5

def move():
  ball.pos+=ball.p * dt/ball.mass
  if not (-side < ball.pos.x < side):
    ball.p.x = -ball.p.x
  if not (-side < ball.pos.y < side):
    ball.p.y = -ball.p.y
  if not (-side < ball.pos.z < side):
    ball.p.z = -ball.p.z
  rate(200,move) # execute the move function about 200 times per second
	
move() # Execute move to start the repetition

print("click on the &lt;div id='pydiv'&gt; tab to see the output")
