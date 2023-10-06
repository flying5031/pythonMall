import requests,re,os,os.path,logging,json
from lxml import etree

#需要下载最新的几个版本,若requirement文件种指定了版本号，则此参数无效：
ver_num = 2
#下载指定的python版本,不指定则填写-1，默认-1,值通常为cp38 ，cp39
ver_python = 'cp38'
#需要批量下载的包的路径，换行分隔。可指定版本号，若不指定版本则ver_num参数生效，例如：requests  2.28.0 或者 requests==2.28.0
download_libs = r'D:\doc\code\py\pythonMall\code\tools\temp\requirement.txt'
#包存储路径
download_path = r"D:\code\downloadlib27"
#包下载源，清华镜像源
download_url = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/'
#阿里镜像源
#download_url = 'http://mirrors.aliyun.com/pypi/simple/'
#豆瓣镜像源
#download_url = 'http://pypi.douban.com/simple/'
#中国科技大学
#download_url = 'https://pypi.mirrors.ustc.edu.cn/simple/'

# 若没有temp目录，则创建此目录。
if not os.path.exists('./temp'):
    os.mkdir('./temp')
    print(r'create directory ./temp')

#设置日志记录
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamhandler = logging.StreamHandler()
filehandler = logging.FileHandler('./temp/downlog.txt',encoding='UTF-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
streamhandler.setFormatter(formatter)
filehandler.setFormatter(formatter)
logger.addHandler(streamhandler)
logger.addHandler(filehandler)

download_url = download_url if download_url.endswith(r'/') else download_url + r'/'
download_url_prefix =download_url.replace('simple/','')

# 如果下载路径不存在，则自动创建
if not os.path.exists(download_path):
    os.makedirs(download_path)
    logger.debug(r'create directory for download,the path is :' + download_path)

#若没有下载过python的包列表，则爬取并保存，否则，直接读取已有文件,避免反复爬取网站数据。
if os.path.exists('./temp/pylib_list.txt') and os.path.getsize('./temp/pylib_list.txt') != 0:
    pyf = open('./temp/pylib_list.txt','r')
    pylibs = pyf.read()
    pylib_list = pylibs.split('\n')
    logger.info('./temp/读取pylib_list成功!')
    pyf.close()
else:
    #将镜像源的包目录保存在当前路径的temp目录中
    resp = requests.request('get',download_url)
    pylib_html = resp.text
    #解析html文件，并保存此列表。
    pylib_list = re.findall('>([\w-]+)</a',pylib_html)
    pylibs = '\n'.join(pylib_list)
    with open('./temp/pylib_list.txt','w') as fp:
        fp.write(pylibs)
        logger.debug('save ./temp/pylib_list.txt success!')



#加载需要下载的包
with open(download_libs) as af:
    down_pkg ={(v:= re.split('\s+|=+',i.strip().lower()))[0] : v[1] if len(v)>1 else '-1' for i in af.read().split('\n')}
    # 正则表达式太慢了，用列表方式比较快
    # pkg_has1 = [v[0] for pkg in all_downlist if (v:=re.findall('^' + pkg + '$',pylibs , flags= re.M|re.I))]
    pkg_has = [pkg for pkg in down_pkg.keys() if pkg in pylib_list]

    logger.info('准备下载的包共：%s 个： %s',len(pkg_has) ,pkg_has)
    pkg_none = set(down_pkg.keys()) - set(pkg_has)
    if pkg_none:
        logger.warning('镜像源中没有的包：%s ' ,pkg_none)
        #将包名中的.替换为-再去查找。如backports.os将会替换为backports-os
        pkg_has_replace = {p:p.replace('.','-') for p in pkg_none if  p.replace('.','-') in pylib_list}
        pkg_has = pkg_has + list(pkg_has_replace.values())
        down_pkg.update({j:down_pkg[i] for i,j in pkg_has_replace.items()})
        pkg_none_replace = pkg_none - set(pkg_has_replace.keys())

        if pkg_none_replace:
            logger.warning('已将镜像中带“.”的包名替换为“-”，镜像源中仍没有的包：%s ', {k:down_pkg[k] for k in pkg_none_replace})

#抓取包的下载链接，下载包
for pkg_name in pkg_has:
    #生成下载路径，若不存在，则创建
    pkg_dir = os.path.join(download_path, pkg_name)
    if not os.path.exists(pkg_dir):
        os.makedirs(pkg_dir)
    response = requests.get(os.path.join(download_url , pkg_name))
    pkg_etree = etree.HTML(response.text)
    a_tag = pkg_etree.xpath('//a')
    #匹配包名及下载链接{'anaconda-client-1.1.1.tar.gz' : 'https://....'}
    pkg_dict = {i.xpath('./text()')[0] : i.xpath('./@href')[0].replace('../../',download_url_prefix) for i in a_tag}
    #过滤macos及win32以及32位linux的包
    pkg_filter = dict(filter(lambda x: len(re.findall('macos|win32|i686' ,x[0])) == 0,pkg_dict.items()))
    #如果指定了版本号，则过滤出此版本'
    ver = down_pkg.get(pkg_name)
    pkg_filter = dict(filter(lambda x:x[0].find(ver) >= 0 ,pkg_filter.items()))
    #如果指定了python的版本，则过滤此版本，若在包列表中未找到指定的版本，则此过滤项无效
    if ver_python != -1:
        pkg_filter_pyver = dict(filter(lambda x: x[0].find(ver_python) >= 0, pkg_filter.items()))
        pkg_filter = pkg_filter_pyver if pkg_filter_pyver else pkg_filter
    # 用正则提取包名的版本号
    pkg_ver_str = {v[0] if (v:=re.findall('-(\d[.0-9]*)[.-]',i)) else '0' for i in pkg_filter}
    # 排序后取最后n个版本
    pkg_ver =list(sorted(pkg_ver_str,key=lambda x:list(map(int,x.split('.'))),reverse=True))[0:ver_num ]
    logger.info('%s 计划下载的版本号为: %s ,准备下载的版本号为： %s',pkg_name,f'最新的{ver_num}个版本' if ver == '-1' else ver, pkg_ver)
    # 取最后n个版本的package
    pkg_filter = dict(filter(lambda x:any([x[0].find(s) >= 0 for s in pkg_ver]),pkg_filter.items()))
    if pkg_filter:
        logger.debug('%s 准备下载的包,共：%s 个:' ,pkg_name ,len(pkg_filter))
        # 开始下载
        for pkg_name, pkg_url in pkg_filter.items():
            pkg_path = os.path.join(pkg_dir, pkg_name)
            if os.path.exists(pkg_path):
                logger.info('已存在此文件: %s', pkg_path)
                continue
            pkg_file = requests.get(pkg_url).content
            if not pkg_file:
                logger.warning('下载失败！文件：%s', pkg_name)
            else:
                logger.info('开始下载: %s', pkg_path)
                fp = open(pkg_path, 'wb')
                fp.write(pkg_file)
                fp.close()
                logger.debug('下载成功，文件大小：%s MB , %s ', round(pkg_file.__sizeof__() / 1024 / 1024, 3), pkg_name)
    else:
        logger.warning('%s 下载失败，镜像源无下载链接！' ,pkg_name)

