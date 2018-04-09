Country = ['Japan', 'United State', 'Italy']
op = '(df["Country"] == "{}")'
opcode_raw = []
for item in Country:
    opcode_raw.append(op.format(item))

opcode_cook = ' | '.join(opcode_raw)

opprint = "print('test')"

print(opcode_cook)
# print(ops)
# op = 'df["Country"] == "Italy"'
# print(op)
#
# print(exec(opprint))
