# -*- encoding: utf-8 -*-   
#@Author      :LiZe
#@File        :ppt.py  
#@Modify Time :2020/4/12 16:49 
#@software    :PyCharm 2020.1



import requests
from bs4 import BeautifulSoup
import os
import time
import sys



def Time_1():     # 进度条函数
    for i in range(1,101):
        sys.stdout.write('\r')
        sys.stdout.write('{0}%|{1}{2}'.format(i,int((i%101)/2)*'-','>'))
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write('\n')

def get_name():
    name=input('请输入你想下载模板的名称(拼音):')
    try:
        os.mkdir('./{}'.format(name))
    except:
        sys.exit()    # 如果程序出错，直接退出程序
    return name

def get_video(name):
    url='https://www.tukuppt.com/videomuban/%s.html'%name
    responce=requests.get(url=url)
    soup=BeautifulSoup(responce.text,'lxml')
    list1=soup.select('div.b-box>dl')    # 列表
    list2=[]    # 用于存储视频链接的列表
    list3=[]

    for i in range(len(list1)):
        str1='http:'+list1[i].select('dd>a>video')[0]['src']   # 一个视频的下载链接
        list2.append(str1)
        str2=list1[i].select('dt.title')[0].get_text()   # 视频的名称
        list3.append(str2)
        print('->【{}】----{}'.format(i+1,str2))

    str_id=input('------>请输入你想下载的视频序号(可输入一连串序号，中将用","隔开):')
    id=[int(i) for i in str_id.split(',')]

    for i in id:
        cb=requests.get(url=list2[i-1]).content    # 用来得到视频的二进制文件 c content b 二进制
        with open(file='./{}/{}.mp4'.format(name,list3[i-1]),mode='wb') as f:
            f.write(cb)
        Time_1()
        print('--->一下载{}.mp4完毕！'.format(list3[i - 1]))

def get_yin(name1):

    url='https://www.tukuppt.com/yinxiaomuban/%s.shtml'%name1
    responce=requests.get(url=url).text
    soup=BeautifulSoup(responce,'lxml')
    list1=soup.select('div.b-box>dl')
    list2=[]
    list3=[]

    for i in range(len(list1)):
        url='http:'+list1[i].select('audio>source')[0]['src']   # 音频下载链接
        name=list1[i].select('dt>a')[0].get_text()
        list2.append(url)
        list3.append(name)
        print('--->【{}】-{}'.format(i+1,name))

    str_id = input('------>请输入你想下载的视频序号(可输入一连串序号，中将用","隔开):')
    id = [int(i) for i in str_id.split(',')]

    for i in id:
        cb = requests.get(url=list2[i - 1]).content  # 用来得到视频的二进制文件 c content b 二进制
        with open(file='./{}/{}.mp3'.format(name1,list3[i - 1]), mode='wb') as f:
            f.write(cb)
        Time_1()
        print('--->一下载{}.mp3完毕！'.format(list3[i - 1]))



if __name__ == '__main__':
    name=get_name()
    print('现在下方有两个选项:')
    print('-->【1】下载视频\n-->【2】下载音频')
    id=int(input('请输入你的选项：'))
    if id==1:
        get_video(name)
    else:
        get_yin(name)




