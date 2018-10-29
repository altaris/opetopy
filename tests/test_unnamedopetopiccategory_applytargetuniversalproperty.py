from UnnamedOpetope import address, Arrow
from UnnamedOpetopicSet import degen, fill, graft, pastingDiagram, point, Sequent
from UnnamedOpetopicCategory import applyTargetUniversalProperty, fillTargetHorn

# Derive a cell degenerate at point a
seq = point(Sequent(), "a")
seq = graft(seq, pastingDiagram(Arrow(), {address('*'): "a"}))
seq = fill(seq, "a", "f")
seq = degen(seq, "a")
seq = fill(seq, "f", "δ")

# Fill the empty pasting diagram at a
seq = degen(seq, "a")
seq = fillTargetHorn(seq, "g", "γ")

# Apply the target universal property of γ
seq = applyTargetUniversalProperty(seq, "γ", "δ", "ξ", "A")

print(seq)
