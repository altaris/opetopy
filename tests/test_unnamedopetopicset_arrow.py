from UnnamedOpetopicSet import Fill, Graft, pastingDiagram, Point, RuleInstance
from UnnamedOpetope import address, Arrow

ar = Point(None, "a")  # type: RuleInstance
ar = Point(ar, "b")
ar = Graft(
    ar, pastingDiagram(
        Arrow(),
        {
            address([], 0): "a"
        }))
ar = Fill(ar, "b", "f")

print(ar.eval())
print()
print(ar.toTex())