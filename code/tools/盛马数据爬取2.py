import requests

login_url = "https://ff.smshj.com/hbshengma/login.html"
# 目标网页URL
target_url = "https://ff.smshj.com/hbshengma/operator/paydetail.html"

# 获取登录页面信息
response = requests.get(login_url)
cookies = response.cookies
# user_agent = response.headers["User-Agent"]

# 构造登录参数
data = {
    "j_username": "18",
    "j_password": ""
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# 登录并判断成功
session = requests.Session()
response = session.post(login_url, data=data, headers=headers, cookies=cookies)
status = response.status_code
rtext = response.text
print("status:",status)
print("rtext:",rtext)
if status == 200 :
    print("登录成功!")
    # 获取登录后的Cookies
    cookies = response.cookies
else:
    print("登录失败!")

# 使用Cookies请求目标网页并爬取
response = session.get(target_url, cookies=cookies, headers=headers)
responsetxt = response.text
with open("paydetail2.html", "w", encoding="utf-8") as f:
    f.write(responsetxt)
# 解析响应并爬取