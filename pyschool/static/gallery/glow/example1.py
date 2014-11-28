from glow import *

_gs=glow('pydiv')
_scene=canvas()

_box=box(color=color.red, pos=vec(1,2,3))
_arrow=arrow(color=color.yellow, pos=vec(3,2,1))
_cylinder=cylinder(color=color.blue, pos=vec(0,0,0))

_sphere=sphere(color=color.blue, pos=vec(7,5,3))

_counter=0
def spin():
    global _counter
    _counter+=1
    _box.rotate(angle=0.01, axis=vec(1,0,0))
    #_box.pos=vec(int((_counter%100)/10), 0, 0)
    _arrow.rotate(angle=0.01, axis=vec(0,1,0))
    _cylinder.rotate(angle=0.01, axis=vec(0,0,1))

    _sphere.pos=vec(0,(_counter%100)/10, 0)

    rate(100, spin)  # make spin a callback       

spin()

print("click on the &lt;div id='pydiv'&gt; tab to see the output")
