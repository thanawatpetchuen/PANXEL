import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time


def time_compare(times, cp_time=1415638800.0):
    tester = times.split('/')
    tes = time.strptime('{}/{}/{}'.format(tester[0], tester[1], tester[2]), '%d/%m/%Y')
    if time.mktime(tes) == cp_time:
        print("YESs")
        return True

file ='global.xlsx'

df = pd.read_excel(file)

df['Order Date'] = pd.to_datetime(df['Order Date'])

opp = "(df['Order Date'] > '2012-01-01') & (df['Order Date'] <= '2012-01-11')"

italdf = df[df['State'] == 'Oklahoma']
ital_filter = df[(df['Order Date'] >= '2014-11-11') & (df['Order Date'] <= '2014-11-12')]
print(ital_filter)
# print(df[((df['Order Date'] > '2012-01-01') & (df['Order Date'] <= '2012-01-11')) & (df['Country'] == 'Italy')])

datecol = [col for col, col_type in df.dtypes.iteritems() if col_type == np.datetime64]
# print("Date Column is ", datecol)

Country = ['Japan', 'United States', 'Italy']
op = '((df["Country"] == "{}") & (time_compare("11/11/2014")))'
opcode_raw = []
for item in Country:
    opcode_raw.append(op.format(item))

opcode_cook = ' | '.join(opcode_raw)

opprint = "print('test')"

# print(opcode_cook)

smulti = df[(df['Country'] == 'Italy') & (time_compare("11/11/2014"))]
multi = df[eval(opcode_cook)]

# print(smulti)
# print(multi)

pt = pd.pivot_table(multi, index="Country", values="Sales", aggfunc=np.sum)
pt.plot(kind="bar")
plt.show()
