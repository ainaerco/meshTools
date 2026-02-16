from random import random

from meshTools.geometry import BBox, Transform, Vector, epsilonTest, solveCubic

v1 = Vector(1, 0, 0)
v2 = Vector(0.00001, 0, 0)
print(v2.zeroTest())
print(epsilonTest(0.01))
print(v1.x)
z = []
for i in range(10):
    z += [Vector(random(), random(), random())]
    print(z[-1])
b = BBox()
b.fromPointSet(z)
print()
print(b[0][0])
print(solveCubic(5, 6, 1, 0))

verts_f = [Vector(3.32413094384e-07, -2.5349085331, -2.5349085331)]
verts_f += [Vector(-2.5349085331, -2.5349085331, -2.216087438e-07)]
verts_f += [Vector(-1.108043719e-07, -2.5349085331, 2.5349085331)]
verts_f += [Vector(2.5349085331, -2.5349085331, 0.0)]
verts_f += [Vector(4.70103117323e-07, 0.0, -3.58490204811)]
verts_f += [Vector(-3.58490204811, 0.0, -3.13402097163e-07)]
verts_f += [Vector(-1.56701048581e-07, 0.0, 3.58490204811)]
verts_f += [Vector(3.58490204811, 0.0, 0.0)]
verts_f += [Vector(3.32413094384e-07, 2.5349085331, -2.5349085331)]
verts_f += [Vector(-2.5349085331, 2.5349085331, -2.216087438e-07)]
verts_f += [Vector(-1.108043719e-07, 2.5349085331, 2.5349085331)]
verts_f += [Vector(2.5349085331, 2.5349085331, 0.0)]
verts_f += [Vector(0.0, -3.58490204811, 0.0)]
verts_f += [Vector(0.0, 3.58490204811, 0.0)]
print()

b.obbFromPointSet(verts_f)

print(b.axis[0], b.axis[1], b.axis[2])

print()
t = Transform()
t.lookAt(Vector(0, 0, 0), Vector(1, 1, 0).normalize(), Vector(0, 1, 0))
# t.translate(Vector(0,0.5,0.3))
# t.rotateAxis(1.4,Vector(0,1,0))
# t.rotateY(1.5)
# t.scale(Vector(1,0.5,0.3))
# t.scaleLocal(0.5,Vector(1,0,0),Vector(1,0,1).normalize())
print(t)
# print t.getEuler()
print(v1.applyTransform(t))
