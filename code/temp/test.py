import re

s = 'numpy  111'
t = s.split('\s')
z = re.split('\s+',s.strip())
print(t)
print(z)