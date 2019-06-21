import sys
sys.path.insert(0, "../")

from opetopy.UnnamedOpetopicSet import Graft, pastingDiagram, Point, \
    RuleInstance, Fill
from opetopy.UnnamedOpetope import address, Arrow, OpetopicInteger, \
    OpetopicTree
from opetopy.UnnamedOpetope import Graft as OptGraft
from opetopy.UnnamedOpetope import Fill as OptShift

# Derivation of ω
omega = OptGraft(
    OptShift(OpetopicInteger(2)),
    OpetopicInteger(2),
    address([['*']]))

# Faster way:
# >>> omega = OpetopicTree([None, [None, None]])

# Derivation of a
classic = Point(None, "a")  # type: RuleInstance

# Derivation of f
classic = Graft(
    classic,
    pastingDiagram(
        Arrow(),
        {
            address([], 0): "a"
        }))
classic = Fill(classic, "a", "f")

# Derivation of α
classic = Graft(
    classic,
    pastingDiagram(
        OpetopicInteger(2),
        {
            address([], 1): "f",
            address(['*']): "f"
        }))
classic = Fill(classic, "f", "α")

# Derivation of β
classic = Graft(
    classic,
    pastingDiagram(
        OpetopicInteger(3),
        {
            address([], 1): "f",
            address(['*']): "f",
            address(['*', '*']): "f"
        }))
classic = Fill(classic, "f", "β")

# Derivation of A
classic = Graft(
    classic,
    pastingDiagram(
        omega,
        {
            address([], 2): "α",
            address([['*']]): "α"
        }))
classic = Fill(classic, "β", "A")

print(classic.eval())
print()
print(classic.toTex())
