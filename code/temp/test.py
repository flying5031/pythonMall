from matplotlib import pyplot as plt

# generate random data
X = np.random.rand(10, 2)

# generate the linkage matrix
Z = linkage(X, 'ward')

# plot dendrogram
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z)
plt.show()
