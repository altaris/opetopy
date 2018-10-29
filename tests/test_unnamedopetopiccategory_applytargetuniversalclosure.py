from UnnamedOpetope import address, Arrow, OpetopicInteger
from UnnamedOpetopicSet import graft, pastingDiagram, point, Sequent
from UnnamedOpetopicCategory import applyTargetUniversalClosure, fillTargetHorn

seq = point(Sequent(), "a")

# Derive a target universal arrow f of source a
seq = graft(seq, pastingDiagram(Arrow(), {address('*'): "a"}))
seq = fillTargetHorn(seq, "b", "f")

# Derive a target universal arrow g of source b
seq = graft(seq, pastingDiagram(Arrow(), {address('*'): "b"}))
seq = fillTargetHorn(seq, "c", "g")

# Compose f and g
seq = graft(
    seq, pastingDiagram(
        OpetopicInteger(2),
        {
            address([], 1): "g",
            address(['*']): "f"
        }))
seq = fillTargetHorn(seq, "h", "α")

# Apply target universality closure
seq = applyTargetUniversalClosure(seq, "α")

print(seq)
