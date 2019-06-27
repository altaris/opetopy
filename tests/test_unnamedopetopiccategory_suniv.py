import sys
sys.path.insert(0, "../")

from opetopy.UnnamedOpetope import address, Arrow, OpetopicInteger
from opetopy.UnnamedOpetopicSet import Graft, pastingDiagram, Point, \
    RuleInstance, Shift
from opetopy.UnnamedOpetopicCategory import TUniv, SUniv, TFill

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

# Derive i, parallel to h
proof = Graft(
    proof, pastingDiagram(
        Arrow(),
        {
            address('*'): "a"
        }))
proof = Shift(proof, "c", "i")

# Derive β
proof = Graft(
    proof, pastingDiagram(
        OpetopicInteger(2),
        {
            address([], 1): "g",
            address(['*']): "f"
        }))
proof = Shift(proof, "i", "β")

# Apply target universality of α over β
proof = TUniv(proof, "α", "β", "ξ", "A")

# Again
proof = TUniv(proof, "α", "β", "ζ", "B")

# Apply source universality of A over B
proof = SUniv(proof, "A", "B", address([], 2), "C", "Ψ")

print(proof.eval())
