import pandas
import pandas as pd

data = [
    ['一队',3,5,2],
    ['二队',3,6,2],
    ['三队一纵队',2,2,3],
    ['三队二纵队',3,1,3],
    ['七队',1,7,3],
    ['四队一纵队',3,2,3],
    ['四队二纵队',3,3,3]
]

df = pandas.DataFrame(data,columns=['name','one','two','three'])
# df = pandas.DataFrame(data)
df.set_index('name',inplace=True)
df2 = df.iloc[:,[1]]
df2.loc[:,'means'] = df.iloc[:,[1]].two.rolling(3).mean()
df2.loc[:,'means2'] = df2.two.rolling(3,min_periods=2).mean()
print(df2)

print('*'*70)
# print(df['two'])
# print(df[2].__class__)
# print(data['one'])
# print(df[1:3])
# print('*'*70)
# print(df.iloc[1:3,1:3]/2)
# print(df.values.tolist().__class__)
