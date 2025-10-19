import requests,json
url1 = ''
link = ''                   #抓登陆包获取登录接口
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
}
res1 = requests.get(url=url1,headers=headers,timeout=5)
if res1.status_code == 200:
    print('网站存活')
    headers1 = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    data = "password=123456&username=admin"   #抓登录包后，根据相应包修改
    res2 = requests.post(url=url+link,headers=headers1,data=data,timeout=5)
    print(res2.text)
    if json.loads(res2.text)["msg"]== "登录成功":
        print("[+]网站存在漏洞！！！")