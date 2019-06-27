import sys
sys.path.insert(0, "../")

from opetopy.NamedOpetope import Graft, Point, Shift

beta = Shift(Graft(
    Shift(Point("c"), "h"),
    Shift(Point("a"), "i"),
    "c"),
    "β")
alpha = Shift(Graft(
    Shift(Point("b"), "g"),
    Shift(Point("a"), "f"),
    "b"),
    "α")
classic = Shift(Graft(beta, alpha, "i"), "A")

print(classic.eval())
print()
print(classic.toTex())
