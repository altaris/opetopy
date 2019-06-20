import sys
sys.path.insert(0, "../")

from opetopy.UnnamedOpetope import address, Arrow, OpetopicInteger
from opetopy.UnnamedOpetopicSet import Graft, pastingDiagram, Point, \
    RuleInstance
from opetopy.UnnamedOpetopicCategory import TClose, TFill

proof = Point(None, "a")  # type: RuleInstance

# Derive a target universal arrow f of source a
proof = Graft(proof, pastingDiagram(Arrow(), {address('*'): "a"}))
proof = TFill(proof, "b", "f")

# Derive a target universal arrow g of source b
proof = Graft(proof, pastingDiagram(Arrow(), {address('*'): "b"}))
proof = TFill(proof, "c", "g")

# Compose f and g
proof = Graft(
    proof, pastingDiagram(
        OpetopicInteger(2),
        {
            address([], 1): "g",
            address(['*']): "f"
        }))
proof = TFill(proof, "h", "α")

# Apply target universality closure
proof = TClose(proof, "α")

print(proof.eval())
