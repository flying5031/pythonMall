import requests
from lxml import etree
import os
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
url = 'https://pic.netbian.com/4kmeinv/index.html'
url_temp = 'https://pic.netbian.com/4kmeinv/index_%d.html'
url_list = [format(url_temp%i) for i in range(2,10)]
url_list.insert(0,url)

for url in url_list:
    resp = requests.get(url,headers = header)
    resp.encoding = 'gbk'
    print('status:',resp.status_code)
    html_text = resp.text
    et = etree.HTML(html_text)
    s = et.xpath('//div[@class="slist"]//a')
    name_url = {el.xpath('.//b/text()')[0] +'.jpg' : 'https://pic.netbian.com/' + el.xpath('./img/@src')[0] for el in s}
    for name,url in name_url.items():
        resp = requests.get(url).content
        with open('save/girl/'+name,'wb') as f:
            f.write(resp)
        print(name,'下载成功！')