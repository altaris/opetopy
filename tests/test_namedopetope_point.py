import sys
sys.path.insert(0, "../")

from opetopy.NamedOpetope import Point

pt = Point("x")
print(pt.eval())
