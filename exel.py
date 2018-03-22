import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data_file = "global.xlsx"
data = pd.read_excel(data_file)

datak = data.keys()
print(datak)

data_ss = data[['Country', 'Category', 'Sales']]
data_sss = data_ss.loc[data_ss['Country'] == "Italy"]
data_cat = data_sss.loc[data_sss['Category'].isin(['Technology'])]
sum_cat = data_sss.groupby('Category')['Sales'].sum()

pdf = data.pivot_table(index=['Country', 'Category'], values=['Sales'], aggfunc=np.sum)

# data_sorted = data_ss.sort_values(['Sales'], ascending=False)
datas = data_sss.sort_values(['Sales'], ascending=[False])
ddss = data_sss.pivot_table(index=['Category'])

print(data_ss)
print(data_sss)
print(sum_cat)
print(data['Country'].unique())
print(pdf)

pdf.head().plot.bar()
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
