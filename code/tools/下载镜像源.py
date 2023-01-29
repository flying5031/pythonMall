import requests,re,os,os.path
from lxml import etree
import os.path

#需要下载最后几个版本：
ver_num = 3
#需要批量下载的包，换行分隔
download_libs = r'D:\doc\code\py\pythonMall\code\tools\temp\acondlib.txt'
#包存储路径
download_path = r"D:\code\pythonlib\acondalibs"
#包下载源，清华镜像源
download_url = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/'
download_prfix_url = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/'


#若没有下载过python的包列表，则爬取并保存，否则，直接读取已有文件,避免反复爬取网站数据。
if os.path.exists('./temp/pylib_list.txt') and os.path.getsize('./temp/pylib_list.txt') != 0:
    pyf = open('./temp/pylib_list.txt','r')
    pylibs = pyf.read()
    pylib_list = pylibs.split('\n')
    print('读取pylib_list成功！')
    pyf.close()
else:
    #如果下载路径不存在，则自动创建
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        print(r'create directory for download,the path is :D:\code\pythonlib\acondalibs')
    #将镜像源的包目录保存在当前路径的temp目录中
    resp = requests.request('get',download_url)
    pylib_html = resp.text
    #若没有temp目录，则创建此目录。
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
        print('create directory ./temp')
    #保存抓取的html文件
    with open(r'./temp/pylib_html', 'w') as fp:
        fp.write(pylib_html)
    #解析html文件，并保存此列表。
    pylib_list = re.findall('>([\w-]+)</a',pylib_html)
    pylibs = '\n'.join(pylib_list)
    with open('./temp/pylib_list.txt','w') as fp:
        fp.write(pylibs)
        print('save pylib_list success!')


with open(download_libs) as af:
    all_downlist =[i.strip().lower() for i in af.read().split('\n')]
    # 正则表达式太慢了，用列表方式比较快
    # pkg_has1 = [v[0] for pkg in all_downlist if (v:=re.findall('^' + pkg + '$',pylibs , flags= re.M|re.I))]
    pkg_has = [pkg for pkg in all_downlist if pkg in pylib_list]
    print('准备下载的包共：' ,len(pkg_has),'个:', pkg_has)
    print('无法下载的包：' ,set(all_downlist) - set(pkg_has))
    print(pkg_has)

#开始下载
for pkg_name in pkg_has:
    #生成下载路径，若不存在，则创建
    pkg_dir = os.path.join(download_path, pkg_name)
    if not os.path.exists(pkg_dir):
        os.makedirs(pkg_dir)
    response = requests.get(os.path.join(download_url , pkg_name))
    pkg_etree = etree.HTML(response.text)
    a_tag = pkg_etree.xpath('//a')
    #匹配包名及下载链接{anaconda-client-1.1.1.tar.gz : https://....}
    pkg_dict = {i.xpath('./text()')[0] : i.xpath('./@href')[0].replace('../../','https://mirrors.tuna.tsinghua.edu.cn/pypi/web/') for i in a_tag}
    #过滤macos的包
    pkg_filtermac = filter(lambda x:x[0].find('macos') == -1 ,pkg_dict.items())
    # 用正则提取包名的版本号
    pkg_ver_str = {v[0] if (v:=re.findall('-(\d[.0-9]*)-',i)) else '0' for i in dict(pkg_filtermac)}
    # 排序后取最后n个版本
    pkg_ver =list(sorted(pkg_ver_str,reverse=True))[0:ver_num ]
    # 取最后n个版本的package
    pkg_filter = filter(lambda x:any([x[0].find(s) >= 0 for s in pkg_ver]),pkg_dict.items())
    #下载包
    download_log = open('./temp/download.log','a')
    for pkg_name, pkg_url in pkg_filter:
        pkg_path = os.path.join(pkg_dir ,pkg_name)
        print('bigen downlaod:----'+pkg_path)
        if os.path.exists(pkg_path):
            continue
        pkg_file = requests.get(pkg_url).content
        fp = open(pkg_path ,'wb')
        fp.write(pkg_file)
        fp.close()
        print('end downlaod:----'+pkg_path)
        download_log.write( pkg_path + ' ,download success： +\n')
    download_log.close()
    # with open(r'D:\python\lib\acondalibs','wb') as fp:
    #
    # print(len(list(pkg_filter)))
    # for i in pkg_dict:
    #     print(re.findall('-(\d[.0-9]*)-',i))
    #
    # hrefs_map = map(lambda x:str.replace(x,r'../../',r'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/'),hrefs)
    # print(list(hrefs_map))
    # print(names)

