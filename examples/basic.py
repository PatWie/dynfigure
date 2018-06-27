from dynfigure import *
from dynfigure.elements import *

"""
Playground
"""

camera = camera.Camera2D()

with CoordinateSystem(xscale=2, yscale=2):
    scene = Scene()
    scene.put(Circle((0, 10), 50, style=Style('red', 'red!0.5!white')))
    scene.put(Circle((0, 10), '50px', style=Style('red', 'red!0.5!white')))
    scene.put(Line([100, 100], [150, 150], style=Style('red', 'red!0.5!white')))

    i = Image('debug.png')
    scene.put(i)

    camera.render(scene).save('test.png')
