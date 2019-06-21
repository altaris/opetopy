import sys
sys.path.insert(0, "../")

from opetopy.UnnamedOpetope import address, Arrow, OpetopicInteger
from opetopy.UnnamedOpetopicSet import Graft, pastingDiagram, Point, \
    RuleInstance, Fill
from opetopy.UnnamedOpetopicCategory import TFill

# Derive points
proof = Point(None, ["a", "b", "c"])  # type: RuleInstance

# Derive f
proof = Graft(
    proof, pastingDiagram(
        Arrow(),
        {
            address('*'): "a"
        }))
proof = Fill(proof, "b", "f")

# Derive g
proof = Graft(
    proof, pastingDiagram(
        Arrow(),
        {
            address('*'): "b"
        }))
proof = Fill(proof, "c", "g")

# Derive the composition cells
proof = Graft(
    proof, pastingDiagram(
        OpetopicInteger(2),
        {
            address([], 1): "g",
            address(['*']): "f"
        }))
proof = TFill(proof, "h", "α")

print(proof.eval())
