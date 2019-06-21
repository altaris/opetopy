import sys
sys.path.insert(0, "../")

from opetopy.NamedOpetope import Graft, Point, Fill

beta = Fill(Graft(
    Fill(Point("c"), "h"),
    Fill(Point("a"), "i"),
    "c"),
    "β")
alpha = Fill(Graft(
    Fill(Point("b"), "g"),
    Fill(Point("a"), "f"),
    "b"),
    "α")
classic = Fill(Graft(beta, alpha, "i"), "A")

print(classic.eval())
print()
print(classic.toTex())
