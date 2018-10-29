from UnnamedOpetope import Arrow, Point, Shift

ar = Shift(Point())

# Faster way
ar = Arrow()

print(ar.eval())
print()
print(ar.toTex())
