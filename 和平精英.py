# -*- coding: utf-8 -*-
# @Time     : 2020/4/6 12:57 
# @Author   : LiZe
# @File     : 和平精英.py 
# @Software : PyCharm


import requests
from bs4 import BeautifulSoup

def get_url():     # 得到想查看的枪械url

    MAIN=True
    url='http://news.4399.com/pubgsy/wqdq/'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
    html=requests.get(url=url,headers=headers)
    html.encoding='gb2312'       # 编码
    soup=BeautifulSoup(html.text,'lxml')
    content=soup.select('div.area.wp.mt10.slide_wp')[0]     # 得到相关枪械的信息

    list1=content.select('ul.cf.slide_nav>li')              # 枪械的种类 如 突击步枪、机枪、狙击枪
    print('--------------欢迎来到和平精英枪械知识库--------------')
    print('相关信息如下：')
    for i in range(len(list1)):
        list1[i]=list1[i].get_text()
        print('【{}】-{}'.format(i+1,list1[i]))
    print('*' * 50)
    id=input('请输入你的选项(输入枪械种类如：步枪、狙击枪或者序号均可):')

    list2=soup.select('ul.clist.l170.cf')    # 所有枪械的信息


    dict1={}   # 构建一个字典，关键字为枪械的种类，值为枪械信息的列表
    for i in range(len(list2)):
        list3=list2[i].select('li>a')
        for j in range(len(list3)):
            list3[j]=[list3[j]['href'],list3[j].get_text()]    # 第一值是枪械的网址、第二个值是枪械的名称
        dict1[list1[i]]=list3


    try:
        list4=dict1[id]    # 你的选择  通过 枪械种类名 查找信息
    except:
        MAIN=False
        pass
    finally:
        if MAIN==False:    # 如果MAIN=False，意味着使用序号查询的，否则用的枪械种类名
            name=list1[int(id)-1]
            list4=dict1[name]
        else:
            name=id
        print('{}-枪械名称如下：'.format(name))
        for i in range(len(list4)):
            print('【{}】--{}'.format(i+1,list4[i][1]))

        print('*' * 50)
        id1=int(input('请输入你想查看的枪械序号:'))-1
        url1=list4[id1][0]

    return url1


def get_info(url):

    html1=requests.get(url=url)
    html1.encoding='gb2312'
    soup1=BeautifulSoup(html1.text,'lxml')    # 枪械介绍

    firearms_introduce=soup1.select('div.area.wp')   # 这是一个列表类型，总长度为4
    soup2=firearms_introduce[0]

    ###########################################################################  枪械介绍
    _list1=soup2.select('div.areabd>div.hreodata>table>tbody>tr.item')

    _list2=_list1[0].select('td')
    str2=''
    for i in range(len(_list2)):
        if (i+1)%2==1:
            str2+=_list2[i].get_text()+':'
        else:
            str2+=_list2[i].get_text()+'\n'

    print(str2)

    for i in range(1,len(_list1)):
        _list3=_list1[i].select('td')
        str2=_list3[0].get_text()+':'+(_list3[1].get_text()).strip('\n')
        if len(str2)>35:
            str2=str2[:35]+'\n'+str2[35:]
        print(str2)

    ###########################################################################  枪械属性

    soup3=firearms_introduce[1]
    _list4=soup3.select('div.skilldata>table>tbody>tr')
    _list5=_list4[0].select('th')
    _list6=_list4[1].select('td')
    for i in range(len(_list5)):
        str1=_list5[i].get_text()+':'+_list6[i].get_text()
        print(str1)
    ###########################################################################  武器伤害

    soup4=firearms_introduce[2]
    _list7=soup4.select('div.skilldata>table>tbody>tr')
    list_1=_list7[0].select('td>strong')
    str3=list_1[0].get_text()
    str4=list_1[1].get_text()
    _list8=_list7[1].select('td')
    _list9=_list7[2].select('td')
    for i in range(len(_list8)):
        if i==0:
            print(str3)
        elif i==4:
            print(str4)

        str1=_list8[i].get_text()+':'+_list9[i].get_text()
        print(str1)




if __name__ == '__main__':
    url=get_url()
    get_info(url)


