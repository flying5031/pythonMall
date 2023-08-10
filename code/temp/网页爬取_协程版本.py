import os
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

BASE_DIR = 'c:/save/requests_apis'
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

visited_urls = set()
path_set = set()

async def get_page(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                content_type = response.headers.get('Content-Type', '')
                if 'text' in content_type or 'application' in content_type:
                    content = await response.text()  # get text content
                else:
                    content = await response.read()  # get binary content
                return response.status, content, content_type
        except Exception as e:
            print(f"Error fetching {url}. Error: {e}")
            return None, None, None


def determine_extension(content_type):
    mime_type = content_type.split(';')[0].strip()
    mapping = {
        'text/html': '.html',
        'text/css': '.css',
        'application/javascript': '.js',
        'image/png': '.png',
        'image/jpeg': '.jpg',
        'image/gif': '.gif'
    }
    return mapping.get(mime_type, '')


def save_to_local(url, content, content_type):
    parsed_url = urlparse(url)
    path = os.path.join(BASE_DIR, parsed_url.netloc, parsed_url.path.lstrip('/'))

    # 为没有明确文件扩展名的URL添加默认扩展名
    if not any(path.endswith(ext) for ext in ['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif']):
        extension = determine_extension(content_type)
        if path.endswith('/'):
            path += 'index' + extension
        else:
            path += extension

    if path in path_set:
        return
    path_set.add(path)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(content)
    print(f"Saved {url} to {path}")
    return path


def extract_css_imports(css_content, css_url):
    import_urls = re.findall(r'@import url\(["\']?(.*?)["\']?\)', css_content)
    return [urljoin(css_url, import_url) for import_url in import_urls]


async def crawl(url, root_url):
    if url in visited_urls:
        return

    status, content, content_type = await get_page(url)
    if status != 200:
        return

    if not content:
        return

    visited_urls.add(url)
    if isinstance(content, str):
        saved_path = save_to_local(url, content.encode(), content_type)
    else:
        saved_path = save_to_local(url, content, content_type)

    if saved_path.endswith('.css'):
        with open(saved_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        import_urls = extract_css_imports(css_content, url)
        for import_url in import_urls:
            await crawl(import_url, root_url)

    soup = BeautifulSoup(content, 'html.parser')
    for link in soup.find_all(['a', 'link', 'script', 'img']):
        href = link.attrs.get('href') or link.attrs.get('src')
        if not href:
            continue
        joined_url = urljoin(url, href)
        if root_url in joined_url and joined_url not in visited_urls:
            await crawl(joined_url, root_url)


def main():
    target_url = 'https://requests.readthedocs.io/en/latest/'
    asyncio.run(crawl(target_url, target_url))


if __name__ == '__main__':
    main()
