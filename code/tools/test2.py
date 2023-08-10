# Welcome to Cursor



# 1. Try generating with command K on a new line. Ask for a pytorch script of a feedforward neural network
# 2. Then, select the outputted code and hit chat. Ask if there's a bug. Ask how to improve.
# 3. Try selecting some code and hitting edit. Ask the bot to add residual layers.
# 4. To try out cursor on your own projects, go to the file menu (top left) and open a folder.

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
                return response.content
        except requests.exceptions.RequestException as e:
            print(e)

    def get_links(self, html):
        try:
            selector = etree.HTML(html)
            links = selector.xpath('//a/@href')
            return links
        except Exception as e:
            print(e)def save_html(self, html, path):
        try:
            with open(path, 'wb') as f:
                f.write(html)
        except Exception as e:
            print(e)

    def run(self):
        html = self.get_html(self.url)
        self.save_html(html, os.path.join(self.save_path, 'index.html'))
        links = self.get_links(html)
        for link in links:
            if link.endswith('.css') or link.endswith('.js') or link.endswith('.png') or link.endswith('.jpg'):
                url = self.url + link
                path = os.path.join(self.save_path, link)
                t = threading.Thread(target=self.download, args=(url, path))
                t.start()


    def download(self, url, path):
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
        except requests.exceptions.RequestException as e:
            print(e)

    def run(self):
        html = self.get_html(self.url)
        links = self.get_links(html)
        for link in links:
            if link.endswith('.css') or link.endswith('.js') or link.endswith('.png') or link.endswith('.jpg'):
                url = self.url + link
                path = os.path.join(self.save_path, link)
                t = threading.Thread(target=self.download, args=(url, path))
                t.start()

if __name__ == '__main__':
    url = 'https://www.python.org/'
    save_path = './python_website'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    crawler = Crawler(url, save_path)
    crawler.run()
