import sys
sys.path.insert(0, "../")

from opetopy.NamedOpetopicSetM import Glue, Pd, Point, RuleInstance, Shift, Sum

p1 = Shift(Pd(Point("a"), "a"), "f")
p1 = Shift(Pd(p1, "a"), "g")

p2 = Shift(Pd(Point("b"), "b"), "h")

example = Sum(p1, p2)  # type: RuleInstance
example = Glue(example, "b", "tf")
example = Glue(example, "b", "tg")
example = Shift(Pd(example, "f"), "ɑ")
example = Glue(example, "b", "ttɑ")
example = Glue(example, "g", "tɑ")
example = Glue(example, "a", "th")

print(example.eval())
print()
print(example.toTex())
