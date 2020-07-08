import requests
from bs4 import BeautifulSoup
from urllib import parse
import json


def get_url():
    # 定有get_url()方法，用于得到读者想下载的视频链接
    keyword=input("请输入你想搜索的关键字:")
    keyword1=parse.urlencode({'keyword':keyword})
    url='https://search.bilibili.com/all?{}'.format(keyword1)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
    response=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(response.text,'lxml')
    urls=soup.select('ul.video-list.clearfix>li>a')  # 搜索得到的列表
    for i in range(len(urls)):
        urls[i]=['https:'+urls[i]['href'],urls[i]['title']]
        print('---->【{}】{}'.format(i+1,urls[i][1]))
    id=int(input('请输入你想下载的视频序号:'))


    return urls[id-1][0] # 视频链接

def get_ips():

    with open(file='ips.txt', mode='r', encoding='utf-8') as f:
        content = f.read()

    ipsList = content.split('\n')  # ip列表
    ipsList2 = []
    for ip in ipsList:
        # 如果ip不是空字符串，则添加到ipsList列表中
        if ip != '':
            ipsList2.append(ip)

    return ipsList2


def get_info(url):
    # 得到所有视频的链接和名称
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
    response=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(response.text,'lxml')
    list_1=soup.select('script')

    info=str(list_1[3])  # 字符出格式的数据
    info=info[info.find('{'):info.rfind('};(function()')+1]
    # 将这个字符串的数据转化为字典格式的数据
    dicInfo=json.loads(info)
    listInfo=dicInfo['videoData']['pages']


    listPage=[]  # 定义一个存储页码的列表

    for i in range(len(listInfo)):
        listPage.append(listInfo[i]['page'])
        listInfo[i]=listInfo[i]['part']  # 视频的名称

    for i in range(len(listPage)):
        listPage[i]=url[:url.rfind('?')]+'?p={}'.format(listPage[i])

    return listPage,listInfo


def get_info1(listPage):
    print('*' * 56)
    print('现在是得到所有视频和音频的请求链接的过程！')
    # 得到所有视频和音频的请求链接
    urlsList=[]

    ipsList=get_ips()
    # 得到ip
    ip = ipsList.pop()
    for url in listPage:
        page=url[url.find('?p=')+3:]
        print('正在爬取页码为{}的数据:'.format(page))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}

        while(True):
            try:
                print('正在使用代理的ip:{}'.format(ip))
                proxies={'http':ip}
                response = requests.get(url=url, headers=headers,proxies=proxies)
                if response.status_code==200:

                    soup = BeautifulSoup(response.text, 'lxml')
                    list_1 = soup.select('script')

                    ## 视频和音频的网址

                    info1 = str(list_1[2])
                    info1 = info1[info1.find('{'):info1.rfind('}') + 1]
                    info1 = json.loads(info1)

                    url1 = info1['data']['dash']['video'][0]['baseUrl']  # 视频的请求链接,选择第一个链接的原因是这个视频的清晰度最高
                    url2 = info1['data']['dash']['audio'][0]['baseUrl']  # 音频的请求链接
                    urlsList.append([url1, url2,page])
                    break
                    # 推出while循环
                else:
                    # 状态码不为200和报错情况下，换一个ip
                    ip=ipsList.pop()

            except Exception as e:
                print('ip:{}无效'.format(ip))
                ip=ipsList.pop()

    return urlsList

def get_info2(urlsList):
    print('*'*56)
    print('---->现在是得到所有视频和音频下载链接的过程！')
    url = 'https://h5seeds-open.xycdn.com/api/get_seeds'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}
    ipsList=get_ips()  # 得到IP
    ip=ipsList.pop()
    infos=[]
    for i in range(len(urlsList)):

        proxies={'http':ip}
        print('正在使用ip:{}爬取{}页内容'.format(ip,urlsList[i][2]))
        while True:
            try:
                data1={'url':urlsList[i][0]}
                response1 = requests.post(url=url, data=json.dumps(data1), headers=headers,proxies=proxies)
                data2 = {'url': urlsList[i][1]}
                response2 = requests.post(url=url, data=json.dumps(data2), headers=headers, proxies=proxies)

                if response1.status_code==200 and response2.status_code==200:
                    dict1 = json.loads(response1.text)
                    dict2=json.loads(response2.text)
                    url_1=dict1['data']['peers'][0]['request_url']  # 视频或者音频的下载链接
                    url_2 = dict2['data']['peers'][0]['request_url']
                    infos.append([url_1,url_2,urlsList[i][2]])
                    break
                else:
                    # 状态码不为200和报错情况下，换一个ip
                    ip=ipsList.pop()
            except Exception as e:
                print('错误原因：{}'.format(e))
                print('ip:{}无效'.format(ip))
                ip = ipsList.pop()

    return infos


# def Download(infos,title,path):#### 使用ip代理的
#     print('*'*56)
#     print('---->现在是下载阶段,时间可能有点久！')
#     ipsList=get_ips()  # ip列表
#     # 将标题与infos相匹配,也可以不匹配
#     for i in range(len(infos)):
#         if (i+1)==int(infos[i][2]):
#             infos[i][2]=title[i]
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}
#
#     videoPath=path[0]
#     audioPath=path[1]
#
#     ip=ipsList.pop()
#     for i in range(len(infos)):
#         print('爬取--->{}'.format(infos[i][2]))
#         while True:
#             print('--->还剩{}个ip'.format(len(ipsList)))
#             proxies={'http':ip}
#             try:
#                 content1=requests.get(url=infos[i][0],headers=headers,proxies=proxies)
#                 time.sleep(1)
#                 content2=requests.get(url=infos[i][1],headers=headers,proxies=proxies)
#                 if content1.status_code==200 and content2.status_code==200:
#                     with open(file=videoPath+'\{}.m4s'.format(infos[i][2]),mode='wb') as f1:
#                         f1.write(content1.content)
#
#                     with open(file=audioPath+'\{}.m4s'.format(infos[i][2]),mode='wb') as f1:
#                         f1.write(content2.content)
#                     print('ip:{}爬取{}->【{}】成功！'.format(ip,i+1,infos[i][2]))
#                     # 如果将两个文件都下载成功，则推出while循环
#                     break
#
#                 else:
#                     print('状态码不是200，更换这个ip：{}'.format(ip))
#                     ip=ipsList.pop()
#
#             except Exception as e:
#                 print('---->ip：{}出错了,错误原因:{}'.format(ip,e))
#                 ip=ipsList.pop()  # 这里可能会出错，最好多准备点ip


def Download(infos,title,path):
    print('*' * 56)
    print('---->现在是下载阶段,时间可能有点久！')
    ipsList = get_ips()  # ip列表
    # 将标题与infos相匹配,也可以不匹配
    for i in range(len(infos)):
        if (i + 1) == int(infos[i][2]):
            infos[i][2] = title[i]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400"}

    videoPath = path[0]
    audioPath = path[1]
    for i in range(len(infos)):
        content1=requests.get(url=infos[i][0],headers=headers)
        content2 = requests.get(url=infos[i][1], headers=headers)

        with open(file=videoPath + '\{}.m4s'.format(infos[i][2]), mode='wb') as f1:
            f1.write(content1.content)

        with open(file=audioPath+'\{}.m4s'.format(infos[i][2]),mode='wb') as f1:
            f1.write(content2.content)
        print('爬取{}->【{}】成功！'.format(i+1,infos[i][2]))


if __name__ == '__main__':
    videoPath=input('请输入存储视频的绝对位置:')
    audioPath=input('请输入存储音频的绝对位置:')
    path=[videoPath,audioPath]
    url=get_url()
    tupel2=get_info(url=url)
    urlsList=get_info1(tupel2[0])
    infos=get_info2(urlsList=urlsList)
    Download(infos=infos,title=tupel2[1],path=path)
