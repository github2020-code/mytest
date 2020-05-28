import requests  # 导入requests模块
from bs4 import BeautifulSoup   # 导入解析模块
from urllib import parse
import threading
import sys
import time


def get_video_content():  # 得到匹配到的相关电影（或者电视剧）的名称、链接、简介的列表
    video=input('请输入你想看的电影或者电视剧名称：')
    keyword=parse.urlencode({'k':video})[2:]   # 对输入的名称进行编码
    url='http://ymystv.com/seacher-%s.html'%(keyword)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
    response=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(response.text,'lxml')
    list_1=soup.select('li.activeclearfix')
    # list_1列表里面有的内容为 电影名称（或者电视剧名称）、链接、简介等
    return list_1

def get_video_contents(list_1:list): # 进一步处理得到的内容（解析）
    list_url=[] # 视频的链接
    listName=[] # 视频名称
    for i in range(len(list_1)):
        url=list_1[i].select('div.detail>h3>a')[0]['href']
        url='http://ymystv.com/'+url[url.rfind('./')+2:]
        list_url.append(url)
        name=list_1[i].select('div.detail>h3>a')[0].text
        listName.append(name)
        print('【{}】-{}'.format(i+1,name)) # 电影或者电视剧的名称
        str1=list_1[i].select('div.detail>div.m-description')[0].text # 电影或者电视剧的简介

        # 对简介进行字符串处理,并按照每行最多50个字符输出
        str1='简介:'+str1[str1.find('简  介 ：')+6:].strip() # 去空格
        for j in range(len(str1)//50+1):
            print('{}'.format(str1[j*50:(j+1)*50]))
        # print('{}'.format(str1)) # 没处理的输出结果
        print('*'+'--'*36)

    id=int(input('请输入你想看的序号:'))

    return list_url[id-1],listName[id-1]

def get_download_json(url:str,name:str): #得到下载视频的json文件
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}  # 请求头
    response=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(response.text,'lxml')

    if '电影' in name:
        urls=[str2['href'] for str2 in soup.select('li.dyli.active>a')]

        if len(urls)==0: # 如果请求的内容长度为0，推出程序，请再一次输入
            print('出错了！')
            sys.exit()

        print('现在，这里有几个下载的源头，请选择其中的一个！')
        for i in range(len(urls)):
            print('【{}】->源头{}'.format(i+1,i+1))
    else:
        urls=[str2['href'] for str2 in soup.select('ul#playlist>li.active>a')]
        list_2=[str3.text for str3 in soup.select('ul#playlist>li.active>a')]
        for i in range(len(list_2)):
            print('【{}】->{}'.format(i+1,list_2[i]))

    id=int(input('输入序号即可:'))-1

    url_1=urls[id]  # 源头

    jiekou='http://jx.ymystv.com/api.php?url='   # 接口

    response_1=requests.get(url=jiekou+url_1,headers=headers)
    print(response_1.status_code)


    if response_1.status_code==200:
        print('成功加载当中！')
        str_url=response_1.json()['url']
    else:
        sys.exit()


    return str_url

def downloads(list_1:list,path:str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}  # 请求头

    while list_1:
        if len(list_1)==0:
            break
        list_2=list_1.pop()
        response = requests.get(url=list_2[1], headers=headers)
        with open(file='{}\{}.ts'.format(path, list_2[0]), mode='wb') as f:
            f.write(response.content)
        print('线程{}正在下载{}.ts'.format(threading.current_thread().getName(),list_2[0]))


def Download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}  # 请求头
    if 'm3u8' in url:
        response=requests.get(url=url,headers=headers)
        path = input('请输入下载的存储路径(绝对路径)：')


        list_1=[str1[:str1.find('\n')] for str1 in response.text.split(',\n')[1:]]
        for i in range(len(list_1)):
            list_1[i]=[i+1,list_1[i]]

        threading_1=[]  # 多线程列表
        for i in range(30):  # 30个线程
            threading1=threading.Thread(target=downloads,args=(list_1,path,))
            threading1.start()
            threading_1.append(threading1)

        for i in threading_1:
            i.join()

        print('所有线程加载完毕！当前现称为{}'.format(threading.current_thread().getName()))

    else:
        print('该链接直接是一个.mp4文件,请直接在浏览器下载！')
        print('链接为:{}'.format(url))





if __name__ == '__main__':

    list_1=get_video_content()
    tuple_1=get_video_contents(list_1)
    url=get_download_json(tuple_1[0],tuple_1[1])
    Download(url)


