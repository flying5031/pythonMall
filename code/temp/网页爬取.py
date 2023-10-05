import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

<<<<<<< HEAD
BASE_DIR = 'api_docs'
=======
BASE_DIR = 'c:/save/requests_api'
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

visited_urls = set()


def get_page(url):
<<<<<<< HEAD
    """获取指定URL的内容及其响应对象"""
=======
    """获取指定URL的内容"""
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully fetched: {url}")
<<<<<<< HEAD
            return response
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
=======
            return response.content
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
    except requests.RequestException as e:
        print(f"Error fetching {url}. Error: {e}")
        return None


<<<<<<< HEAD
def determine_extension(content_type):
    """根据Content-Type确定文件扩展名"""
    mapping = {
        'text/html': '.html',
        'text/css': '.css',
        'application/javascript': '.js',
        'image/png': '.png',
        'image/jpeg': '.jpg',
        'image/gif': '.gif'
    }
    return mapping.get(content_type, '')


def save_to_local(url, response):
    """保存内容到本地文件系统"""
    parsed_url = urlparse(url)
    path = os.path.join(BASE_DIR, parsed_url.netloc, parsed_url.path.lstrip('/'))
    if not any(path.endswith(ext) for ext in ['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif']):
        extension = determine_extension(response.headers.get('Content-Type', ''))
        path += extension
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(response.content)
=======
def save_to_local(url, content):
    """保存内容到本地文件系统"""
    parsed_url = urlparse(url)
    path = os.path.join(BASE_DIR, parsed_url.netloc, parsed_url.path.lstrip('/'))
    if not path.endswith(('.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif')):
        if parsed_url.path.endswith('/'):
            path += 'index.html'
        else:
            path += '.html'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(content)
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
    print(f"Saved {url} to {path}")


def crawl(url, root_url):
    """递归爬取指定URL的内容和资源"""
    if url in visited_urls:
        return

<<<<<<< HEAD
    response = get_page(url)
    if not response:
        return

    visited_urls.add(url)
    save_to_local(url, response)

    soup = BeautifulSoup(response.content, 'html.parser')
=======
    content = get_page(url)
    if not content:
        return

    visited_urls.add(url)
    save_to_local(url, content)

    soup = BeautifulSoup(content, 'html.parser')
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
    # 查找页面中的所有链接和资源
    for link in soup.find_all(['a', 'link', 'script', 'img']):
        href = link.attrs.get('href') or link.attrs.get('src')
        if not href:
            continue
        joined_url = urljoin(url, href)
        if root_url in joined_url and joined_url not in visited_urls:
            crawl(joined_url, root_url)


def main():
    """主函数，开始爬虫任务"""
<<<<<<< HEAD
    target_url = 'https://docs.python.org/3/'  # 示例URL，替换为目标API文档的URL
=======
    target_url = 'https://requests.readthedocs.io/en/latest/'  # 示例URL，替换为目标API文档的URL
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
    crawl(target_url, target_url)


if __name__ == '__main__':
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 0685f24f37d1a1b0d4d18432a4ce5a397d850f37
