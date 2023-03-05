import re
import numpy
import pandas as pd
s = 'numpy  111'
t = s.split('\s')
z = re.split('\s+',s.strip())
print(t)
print(z)

a = pd.Series(numpy.zeros(7+1) +1)
print(a)