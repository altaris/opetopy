from UnnamedOpetope import address, Arrow, OpetopicInteger
from UnnamedOpetopicSet import Graft, pastingDiagram, Point, \
    RuleInstance, Shift
from UnnamedOpetopicCategory import TFill

# Derive points
proof = Point(None, ["a", "b", "c"])  # type: RuleInstance

# Derive f
proof = Graft(
    proof, pastingDiagram(
        Arrow(),
        {
            address('*'): "a"
        }))
proof = Shift(proof, "b", "f")

# Derive g
proof = Graft(
    proof, pastingDiagram(
        Arrow(),
        {
            address('*'): "b"
        }))
proof = Shift(proof, "c", "g")

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
