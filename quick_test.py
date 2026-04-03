from rpgnlp import NLPEngine
e = NLPEngine()
r = e.run("go north")
print("TYPE:", type(r))
print("VAL:", r)
r2 = e.run("go to the north gate")
print("TYPE2:", type(r2))
print("VAL2:", r2)
