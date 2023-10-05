from scrapeasy import Website, Page
webs = Website("https://blog.csdn.net/wuyoudeyuer?type=blog")
webs.download('img',r'C:\\save')

w3 = Page("https://blog.csdn.net/")
w3.download('txt',r'c:\save')
