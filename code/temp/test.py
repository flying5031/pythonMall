<<<<<<< HEAD
download_url = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple'

download_url = download_url if download_url.endswith(r'/') else download_url + r'/'

print(download_url)
a = download_url.replace('simple/','')
print(a)

=======
from matplotlib import pyplot as plt

# generate random data
X = np.random.rand(10, 2)

# generate the linkage matrix
Z = linkage(X, 'ward')

# plot dendrogram
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z)
plt.show()
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
