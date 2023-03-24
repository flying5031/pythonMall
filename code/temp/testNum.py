import numpy as np
# from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import matplotlib.pylab as plt
import matplotlib;matplotlib.rc('font',family='Microsoft Yahei')
import pandas as pd

a = '''3822. 3820. 3811. 3809. 3803. 3808. 3795. 3800. 3806. 3804. 3810. 3804.
 3805. 3810. 3807. 3806. 3808. 3810. 3814. 3819. 3811. 3808. 3815. 3817.
 3827. 3826. 3832. 3828. 3828. 3825. 3818. 3803. 3809. 3810. 3814. 3816.
 3811. 3813. 3831. 3820. 3804. 3806. 3829. 3812. 3807. 3788. 3786. 3791.
 3785. 3780. 3791. 3782. 3790. 3795. 3799. 3789. 3786. 3789. 3789. 3790.
 3791. 3798. 3799. 3810. 3820. 3813. 3814. 3814. 3818. 3819. 3811. 3813.
 3814. 3825. 3825. 3830. 3826. 3830. 3827. 3828. 3824. 3830. 3828. 3835.
 3844. 3848. 3839. 3868. 3878. 3877. 3879. 3875. 3884. 3873. 3874. 3881.
 3885. 3882. 3881. 3879. 3883. 3892. 3894. 3894. 3913. 3923. 3922. 3922.
 3923. 3932. 3923. 3925. 3925. 3944. 3947. 3953. 3952. 3936. 3929. 3936.
 3942. 3945. 3943. 3951. 3944. 3942. 3958. 3956. 3965. 3960. 3980. 3982.
 3986. 3979. 3937. 3950. 3949. 3945. 3941. 3939. 3948. 3945. 3942. 3922.
 3924. 3922. 3935. 3937. 3938. 3936. 3938. 3936. 3932. 3930. 3933. 3934.
 3935. 3939. 3945. 3951. 3954. 3943. 3938. 3946'''

b = a.split('.')
close_price = [int(i.strip()) for i in b]
# z = sch.linkage(c,metric='euclidean',method='single')
# print(z)
df = pd.DataFrame(close_price)
df2 = df[0:20]
maxd = df2.rolling(3).max()
maxd.rename(columns={0:'price'},inplace=True)
mind = df2.rolling(3).min()
mind.rename(columns={0:'price'},inplace=True)

# print(maxd)
#需要以下步骤以两列格式准备数据。
maxdf = pd.concat([maxd,pd.Series(np.zeros(len(maxd))+1)],axis = 1)
mindf = pd.concat([mind,pd.Series(np.zeros(len(mind))+-1)],axis = 1)
# print(maxdf)
# maxdf.drop_duplicates('price',inplace = True)
# mindf.drop_duplicates('price',inplace = True)
# print(maxdf)
# print(mindf)


F = maxdf.append(mindf).sort_index()

F = F[ F[0] != F[0].shift() ].dropna()
print(F.price.values.reshape(-1,1))


X = np.concatenate((F.price.values.reshape(-1,1),
                    (np.zeros(len(F))+1).reshape(-1,1)), axis = 1 )
print('*'*70)
cluster = AgglomerativeClustering(n_clusters=3,affinity='euclidean', linkage='average')
cluster.fit_predict(X)

F['clusters'] = cluster.labels_

F2 = F.loc[F.groupby('clusters')['price'].idxmax()]
print(F2.itertuples)

fig, axis = plt.subplots()
for row in F2.itertuples():
    axis.axhline(y=row.price,
                 color='green', ls='dashed')

axis.plot(F.index.values, F.price.values)
plt.show()