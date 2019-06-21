import sys
sys.path.insert(0, "../")

from opetopy.UnnamedOpetope import address, Arrow
from opetopy.UnnamedOpetopicSet import Degen, Graft, pastingDiagram, Point, \
    RuleInstance, Fill
from opetopy.UnnamedOpetopicCategory import TUniv, TFill

# Derive a cell degenerate at point a
proof = Point(None, "a")  # type: RuleInstance
proof = Graft(proof, pastingDiagram(Arrow(), {address('*'): "a"}))
proof = Fill(proof, "a", "f")
proof = Degen(proof, "a")
proof = Fill(proof, "f", "δ")

# Fill the empty pasting diagram at a
proof = Degen(proof, "a")
proof = TFill(proof, "g", "γ")

# Apply the target universal property of γ
proof = TUniv(proof, "γ", "δ", "ξ", "A")

print(proof.eval())
