from UnnamedOpetope import address, Arrow, OpetopicInteger
from UnnamedOpetopicSet import fill, graft, pastingDiagram, point, Sequent
from UnnamedOpetopicCategory import fillTargetHorn

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

print(seq)
