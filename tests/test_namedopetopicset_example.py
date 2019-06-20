import sys
sys.path.insert(0, "../")

from opetopy.NamedOpetope import Point, Shift
from opetopy.NamedOpetopicSet import Glue, Repr, Sum

alpha = Shift(Shift(Point("a"), "f"), "α")
g = Shift(Point("c"), "g")
h = Shift(Point("b"), "h")
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
