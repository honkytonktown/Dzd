import pandas as pd

df = pd.DataFrame({'ID':['1', '2', '3'], 'col_1': [0, 2, 3], 'col_2':[1, 4, 5]})
mylist = ['a', 'b', 'c', 'd', 'e', 'f']

def get_sublist(sta,end):
    return mylist[sta:end+1]

df['col_3'] = df.apply(lambda x: get_sublist(x.col_1, x.col_2), axis=1)
print(df)