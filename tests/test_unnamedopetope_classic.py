from UnnamedOpetope import address, Graft, OpetopicInteger, Shift

classic = Graft(
    Shift(OpetopicInteger(2)),
    OpetopicInteger(2),
    address([['*']])
)
# Faster way: classic = OpetopicTree([None, [None, None]])

print(classic.eval())
print()
print(classic.toTex())
