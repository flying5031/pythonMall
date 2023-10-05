# -*- coding: utf-8 -*-
import requests
import os
import threading
from lxml import etree

class Crawler:
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.session = requests.Session()

    def get_html(self, url):
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except requests.exceptions.RequestException as e:
            print('网站加载失败：')
            print(e)

    def get_links(self, html):
        try:
            selector = etree.HTML(html)
            # links = selector.xpath('//a/@href |//img/@src | //script/@src | //link@href')
            links = selector.xpath('//a/@href | //img/@src | //script/@src | //link/@href')
            print('links:',links)
            return links
        except Exception as e:
            print('网站解析失败：')
            print(e)

    def download(self, url, path):
        try:
            print('download url is:',url,'save path is:',path)
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
        except requests.exceptions.RequestException as e:
            print('下载失败：')
            print(e)

    def run(self):
        html = self.get_html(self.url)
        links = self.get_links(html)
        for link in links:
            if link.endswith('.css') or link.endswith('.js') or link.endswith('.png') or link.endswith('.jpg') or link.endswith('.html'):
                # url = self.url + link
                if link.startswith('//') :
                    url = 'http:' + link
                else:
                    url = link
                path = os.path.join(self.save_path, os.path.basename(link))
                print('')
                t = threading.Thread(target=self.download, args=(url, path))
                t.start()

if __name__ == '__main__':
    url = 'https://docs.python.org/zh-cn/3/'
    save_path = r'D:\360Downloads\website'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    crawler = Crawler(url, save_path)
    crawler.run()
