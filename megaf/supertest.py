import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file ='global.xlsx'

df = pd.read_excel(file)

Country = ['Japan', 'United States', 'Italy']
op = '(df["Country"] == "{}")'
opcode_raw = []
for item in Country:
    opcode_raw.append(op.format(item))

opcode_cook = ' | '.join(opcode_raw)

opprint = "print('test')"

print(opcode_cook)

# multi = df[(df['Country'] == 'Italy') | (df['Country'] == 'Japan')]
multi = df[eval(opcode_cook)]

print(multi)

pt = pd.pivot_table(multi, index="Country", values="Sales", aggfunc=np.sum)
pt.plot(kind="hist")
plt.show()
