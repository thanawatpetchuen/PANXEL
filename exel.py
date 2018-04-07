import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data_file = "global.xlsx"
data = pd.read_excel(data_file)

datak = data.keys()
print(datak)

print(data.Country.unique())

data_ss = data[['Country', 'Category', 'State', 'Sales']]
data_sss = np.where((data['Country'] == 'Italy') | (data['Country'] == 'Japan'))
# data_sss = data.loc[data['Country'] == "Italy" | data['Country'] == 'Japan']
state = data_ss.loc[data['State'] == 'Oklahoma']
# data_cat = data_sss.loc[data_sss['Category'].isin(['Technology'])]
# sum_cat = data_sss.groupby('Category')['Sales'].sum()
#
pdf = data_sss.pivot_table(index=['Country', 'Category'], values=['Sales'], aggfunc=np.sum)
#
# data_sorted = data_ss.sort_values(['Sales'], ascending=False)
# datas = data_sss.sort_values(['Sales'], ascending=[False])
# ddss = data_sss.pivot_table(index=['Category'])

# print(data_sss)
# print(data_sss['State'].unique())



# py = data.groupby(['Country', 'State']).size()
# pyi = py.pivot_table(index=py, values=['Sales'])
# py.plot.bar()
# plt.show()

# print(data_sss)
# print(sum_cat)
# print(data['Country'].unique())
# print(pdf)

pdf.plot.bar()
plt.show()

# print((data[['Country']]))
# for i in data[['Country']]:
#     print(i)
# ddss.plot(kind="bar")
# plt.show()
# print(datas)
# data_sss.head().plot.bar()
# sum_cat.plot.bar(title="Italy")
# plt.show()
