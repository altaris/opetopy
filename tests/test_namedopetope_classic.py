from NamedOpetope import Fill, Graft, Point

beta = Fill(Graft(
    Fill(Point("c"), "h"),
    Fill(Point("a"), "i"),
    "c"),
    "β")
alpha = Fill(Graft(
    Fill(Point("b"), "g"),
    Fill(Point("a"), "f"),
    "b"),
    "α")
classic = Fill(Graft(beta, alpha, "i"), "A")

print(classic.eval())
print()
print(classic.toTex())
