from NamedOpetopicSetM import Fill, Glue, Pd, Point, RuleInstance, Sum

p1 = Fill(Pd(Point("a"), "a"), "f")
p1 = Fill(Pd(p1, "a"), "g")

p2 = Fill(Pd(Point("b"), "b"), "h")

example = Sum(p1, p2)  # type: RuleInstance
example = Glue(example, "b", "tf")
example = Glue(example, "b", "tg")
example = Fill(Pd(example, "f"), "ɑ")
example = Glue(example, "b", "ttɑ")
example = Glue(example, "g", "tɑ")
example = Glue(example, "a", "th")

print(example.eval())
print()
print(example.toTex())
