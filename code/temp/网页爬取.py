import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

BASE_DIR = 'api_docs'
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

visited_urls = set()


def get_page(url):
    """获取指定URL的内容及其响应对象"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully fetched: {url}")
            return response
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching {url}. Error: {e}")
        return None


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
    print(f"Saved {url} to {path}")


def crawl(url, root_url):
    """递归爬取指定URL的内容和资源"""
    if url in visited_urls:
        return

    response = get_page(url)
    if not response:
        return

    visited_urls.add(url)
    save_to_local(url, response)

    soup = BeautifulSoup(response.content, 'html.parser')
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
    target_url = 'https://docs.python.org/3/'  # 示例URL，替换为目标API文档的URL
    crawl(target_url, target_url)


if __name__ == '__main__':
    main()