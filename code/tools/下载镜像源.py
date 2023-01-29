import requests
import re,os
from lxml import etree
import os.path

#包存储路径
path = r"D:\python\lib\acondalibs"
#包下载源，清华镜像源
download_url = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/'
#将镜像源的包目录全部保存下来
report = requests.request('get','https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/')
report_txt = report.text
text_str = str(report_txt).split('\n')
if not os.path.exists('temp'):
    os.mkdir('temp')
with open(r'save/python_package/result.txt', 'w') as fp:
    fp.write(report_txt)
with open('save/python_package/requirement.txt', 'w+') as f:
    for i in text_str:
        temp = re.findall('<a href="(.*?)/">',i)
        # print(i,temp)
        if temp != []:
            f.write(str(temp[0])+'\n')

# with open('save/pypkg/anaconda.txt') as af:
#     ac_pkgname = af.readline()
#
# acon_file = open('save/pypkg/anaconda.txt','r',encoding='utf-8')
# qinghua_requ = open('save/pypkg/anaconda.txt','r',encoding='utf-8')
# qinghua_txt = qinghua_requ.read()
# print(re.findall('^pandas',qinghua_txt,flags=re.M))
#
# acon_file.close()
# qinghua_requ.close()

# response = requests.get("https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/pandas/")
# text = response.text
# with open('save/pypkg/pkglist.txt','w',encoding='utf-8') as af:
#     af.write(text)

with open('save/pypkg/pkglist.txt','r',encoding='utf-8') as af:
    pkg_etree = etree.HTML(af.read())
    a_tag = pkg_etree.xpath('//a')
    #匹配包名及下载链接
    pkg_dict = {i.xpath('./text()')[0] : i.xpath('./@href')[0].replace('../../','https://mirrors.tuna.tsinghua.edu.cn/pypi/web/') for i in a_tag}
    #过滤macos的包
    pkg_filtermac = filter(lambda x:x[0].find('macos') == -1 ,pkg_dict.items())
    # 用正则提取包名的版本号
    pkg_ver_str = {v[0] if (v:=re.findall('-(\d[.0-9]*)-',i)) else '0' for i in dict(pkg_filtermac)}
    # 排序后取最后3个版本
    pkg_ver = list(sorted(pkg_ver_str,reverse=True))[0:3]
    # 取最后3个版本的package
    pkg_filter = filter(lambda x:any([x[0].find(s) >= 0 for s in pkg_ver]),pkg_dict.items())
    #下载包
    for pkg in pkg_filter:
        pkg_path = path + '\\'[:-1] + pkg[0]
        print('bigen downlaod:----'+pkg_path)
        pkg_file = requests.get(pkg[1]).content
        fp = open(pkg_path ,'wb')
        fp.write(pkg_file)
        fp.close()
        print('end downlaod:----'+pkg_path)

    # with open(r'D:\python\lib\acondalibs','wb') as fp:

    # print(len(list(pkg_filter)))
    # for i in pkg_dict:
    #     print(re.findall('-(\d[.0-9]*)-',i))

# hrefs_map = map(lambda x:str.replace(x,r'../../',r'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/'),hrefs)
# print(list(hrefs_map))
# print(names)

