import pandas as pd
from appJar import *
import warnings
import matplotlib.pyplot as plt

data = pd.read_excel("global.xlsx")

data_ss = data[['City', 'Sales']]
data_sorted = data_ss.sort_values(['Sales'], ascending=[False])[['City', 'Sales']]
print(data_sorted)

ddss = data_sorted.head(10).pivot_table(index=['City'])
# ddss = data_sorted.head(10).plot.bar()
ddss.plot(kind="bar")
plt.show()
