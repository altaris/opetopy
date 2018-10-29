from NamedOpetope import Fill, Point
from NamedOpetopicSet import Fold, Repr, Sum

alpha = Fill(Fill(Point("a"), "f"), "α")
g = Fill(Point("c"), "g")
h = Fill(Point("b"), "h")
unfolded = Sum(Sum(Repr(alpha), Repr(g)), Repr(h))
example = Fold(Fold(Fold(Fold(Fold(unfolded,
                                   "a",
                                   "c"),
                              "b",
                              "tf"),
                         "b",
                         "tg"),
                    "a",
                    "th"),
               "g",
               "tα")

print(example.eval())
print()
print(example.toTex())
