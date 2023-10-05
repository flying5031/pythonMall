import requests
from bs4 import BeautifulSoup

# 登录页面URL
login_url = "https://ff.smshj.com/hbshengma/user/login.action"
# 目标网页URL
target_url = "https://ff.smshj.com/hbshengma/operator/paydetail.html"

# 登录参数
data = {
    "j_username": "",
    "j_password": ""
}

# 设置User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# 登录并获取登录状态
session = requests.Session()
response = session.post(login_url, data=data, headers=headers)
status_code = response.status_code
print('status_code:',status_code)
if status_code == 200:
    print("登录成功!")
    cookies = response.cookies

    # 使用登录后的Cookie请求目标网页
    response = session.get(target_url, cookies=cookies, headers=headers)
    responsetxt = response.text
    # 解析目标网页内容
    soup = BeautifulSoup(responsetxt, "html.parser")
    # content = soup.find(id="payDetail").find_all("tr")

    # 写入文件
    with open("paydetail.html", "w", encoding="utf-8") as f:
            f.write(responsetxt)

    print("爬取内容已保存到paydetail.txt文件中!")
else:
    print("登录失败!")