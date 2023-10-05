import requests
from bs4 import BeautifulSoup
import os
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

url = "https://www.zcool.com.cn/work/ZNjQzOTU2NzY=.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
images = soup.find_all("img")

if not os.path.exists("D:/360Downloads/pic"):
    os.makedirs("D:/360Downloads/pic")

for image in images:
    image_url = image["src"]
    if image_url.startswith("//"):
        image_url = "https:" + image_url
    elif not image_url.startswith("http"):
        image_url = url + image_url
    response = requests.get(image_url)
    with open("D:/360Downloads/pic/" + image_url.split("/")[-1], "wb") as f:
        f.write(response.content)
        print("Saved file:", f.name)

