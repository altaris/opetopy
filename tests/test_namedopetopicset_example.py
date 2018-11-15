from NamedOpetope import Fill, Point
from NamedOpetopicSet import Glue, Repr, Sum

alpha = Fill(Fill(Point("a"), "f"), "α")
g = Fill(Point("c"), "g")
h = Fill(Point("b"), "h")
unglued = Sum(Sum(Repr(alpha), Repr(g)), Repr(h))
example = Glue(Glue(Glue(Glue(Glue(unglued,
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
