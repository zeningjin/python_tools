# coding=utf-8
import pandas as pd
import numpy as np

data = np.arange(1, 101).reshape((10, 10))
print(data)
data_df = pd.DataFrame(data)
print(data_df)
data_df.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
data_df.index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

#
# data = {'h':{'a':1, 'b':2}, 'd':{'a':1, 'b':2}, 'f':{'a':1, 'b':2}, 'u':{'a':1, 'b':2}}
# data_df = pd.DataFrame(data)
# print(data_df)

writer = pd.ExcelWriter('my.xlsx')
data_df.to_excel(writer, float_format='%.5f')
writer.save()
