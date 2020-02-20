import sys
sys.path.insert(0, "../")

from opetopy.UnnamedOpetope import address, Graft, OpetopicInteger, OpetopicTree, Shift

classic = Graft(
    Shift(OpetopicInteger(2)),
    OpetopicInteger(2),
    address([['*']])
)
# Faster way:
# >>> classic = OpetopicTree([None, [None, None]])

print(classic.eval())
