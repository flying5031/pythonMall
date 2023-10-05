download_url = 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple'

download_url = download_url if download_url.endswith(r'/') else download_url + r'/'

print(download_url)
a = download_url.replace('simple/','')
print(a)

