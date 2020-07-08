import requests
from bs4 import BeautifulSoup
import threading


def getIP(JS):
    ## 定义getIP方法，用于得到IP信息
    ipInfo = []

    for j in range(1,JS+1):
        url='https://www.kuaidaili.com/free/inha/%d/'%(j)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
        try:
            content=requests.get(url=url,headers=headers)
            if content.status_code==200:
                print("-->访问第{}页成功！".format(j))
                soup=BeautifulSoup(content.text,'lxml')
                str_1=soup.select('table.table.table-bordered.table-striped')  # 相关IP的列表，长度为1
                IP=[ip.text for ip in str_1[0].select('tbody>tr>td[data-title="IP"]')]   # IP号
                PORT=[PORT.text for PORT in str_1[0].select('tbody>tr>td[data-title="PORT"]')]  # 端口号

                for i in range(len(IP)):
                    ipInfo.append(IP[i]+':'+PORT[i])
            else:
                print("-->访问第{}页失败！".format(j))

        except Exception as e:
            print("出错了，错误原因:{}".format(e))

    return ipInfo

def PD(ipInfo:list):
    while True:
        if len(ipInfo)==0:
            break

        ip=ipInfo.pop()  # 一个ip
        url = 'https://www.baidu.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
        proxies = {'http':ip}
        try:
            response=requests.get(url=url, headers=headers, proxies=proxies,timeout=5)   # 超时时间为5秒
            print('【线程{}】-->正在判断IP为{}是否可用'.format(threading.current_thread().getName(),ip))
            print(response.status_code)
            if response.status_code==200:
                with open(file='./ips.txt',mode='a',encoding='utf-8') as f:
                    f.write(ip+'\n')

        except Exception as e:
            print("出错了，错误原因:{}".format(e))


def writeIP(ipInfo):
    ## 定义writeIP方法，用于将可用的IP信息写入到一个文件中
    tList=[]   # 定义线程列表
    for i in range(10): # 定义10个线程
        threading_1=threading.Thread(target=PD,args=(ipInfo,))
        tList.append(threading_1)
        threading_1.start()
    for i in tList:
        i.join()
    print('当前线程为：{}'.format(threading.current_thread().getName()))

if __name__ == '__main__':
    JS=int(input('请输入你想爬取的IP页数:'))
    ipInfo=getIP(JS=JS)
    print(len(ipInfo))
    print('爬取ip已结束，现在是验证ip')
    writeIP(ipInfo=ipInfo)
