import pip
from subprocess import call

with open(r'D:\python\pylib-conda\requirements.txt','r',encoding='utf-8') as f:
    # lines = f.readline()
    for line in f:
        pip_name = "pip download " + line + " --index-url https://mirrors.aliyun.com/pypi/simple/  -d 'D:\python\pylib-conda' "
        print(pip_name)
        call(pip_name, shell=True)