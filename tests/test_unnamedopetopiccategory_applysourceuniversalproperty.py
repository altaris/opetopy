from UnnamedOpetope import address, Arrow, OpetopicInteger
from UnnamedOpetopicSet import fill, graft, pastingDiagram, point, Sequent
from UnnamedOpetopicCategory import applyTargetUniversalProperty, \
    applySourceUniversalProperty, fillTargetHorn

# Derive points
seq = point(Sequent(), ["a", "b", "c"])

# Derive f
seq = graft(
    seq, pastingDiagram(
        Arrow(),
        {
            address('*'): "a"
        }))
seq = fill(seq, "b", "f")

# Derive g
seq = graft(
    seq, pastingDiagram(
        Arrow(),
        {
            address('*'): "b"
        }))
seq = fill(seq, "c", "g")

# Derive the composition cells
seq = graft(
    seq, pastingDiagram(
        OpetopicInteger(2),
        {
            address([], 1): "g",
            address(['*']): "f"
        }))
seq = fillTargetHorn(seq, "h", "α")

# Derive i, parallel to h
seq = graft(
    seq, pastingDiagram(
        Arrow(),
        {
            address('*'): "a"
        }))
seq = fill(seq, "c", "i")

# Derive β
seq = graft(
    seq, pastingDiagram(
        OpetopicInteger(2),
        {
            address([], 1): "g",
            address(['*']): "f"
        }))
seq = fill(seq, "i", "β")

# Apply target universality of α over β
seq = applyTargetUniversalProperty(seq, "α", "β", "ξ", "A")

# Again
seq = applyTargetUniversalProperty(seq, "α", "β", "ζ", "B")

# Apply source universality of A over B
seq = applySourceUniversalProperty(seq, "A", "B", address([], 2), "C", "Ψ")

print(seq)
