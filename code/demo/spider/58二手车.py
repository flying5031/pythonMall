import requests
from lxml import etree
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
url = 'https://cq.58.com/ershouche/?PGTID=0d100000-0002-58c4-b577-5c78aa0d2e8c&ClickID=2'

resp = requests.get(url,headers=header)
print(resp.status_code)
text = resp.text
print(text)
with open('save/58car.html','w',encoding='utf-8') as f:
    f.write(text)
# es = etree.HTML(text)
#
# s = es.xpath('//li[contains(@data-showlog,"esc_xlist_hp_show_jgg")')
#
# print(s)