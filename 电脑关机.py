import requests
from bs4 import BeautifulSoup
import os
import time


def get_info():
   url='收邮件的那个网址'
    headers={
        'cookie':'邮箱cookie',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
    }
    html_2=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(html_2.text,'lxml')
    list_1=soup.select('div#div_showtoday>table.i.F')
    info=list_1[0]
    name=info.select('td.tl.tf>nobr>span')[0].get_text()   #发件人
    zhuti=info.select('td.gt>div.tf.no>u')[0].get_text()  # 发件的主题
    return name,zhuti


if __name__ == '__main__':
    while True:
        tuple=get_info()
        print(tuple)
        name,zhuti=tuple[0],tuple[1]
        if '发件人' in name and '关机' in zhuti:
            os.system('shutdown -s -t 1')
        else:
            pass
        time.sleep(300)   # 每运行一次,休眠5分钟
