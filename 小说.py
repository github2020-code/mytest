import requests
from bs4 import BeautifulSoup
from urllib import parse
import os
import threading


def matching_book(): # 得到所有匹配到的小说
    keyword = input('请输入你想下载的小说标题:')
    key_word = parse.urlencode({'keyword': keyword})
    url='http://search.zongheng.com/s?%s'%(key_word)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    html=requests.get(url=url,headers=headers)
    info=html.text     # 网页信息
    soup=BeautifulSoup(info,'lxml')
    list_1=soup.select('div.search-tab>div.search-result-list.clearfix')   # 小说信息
    book_url=[]
    book_name=[]
    for i in range(len(list_1)):
        str_1=list_1[i].select('div.fl.se-result-infos>h2>a')[0]['href']       # 小说的网址
        name_1=list_1[i].select('div.fl.se-result-infos>h2>a')[0].get_text()   # 匹配到的小说名称
        book_url.append(str_1)
        book_name.append(name_1)
        print('【{}】-{}'.format(i+1,name_1))

    id=int(input('请输入你想看的小说序号:'))

    return book_url[id-1],book_name[id-1]

def get_catalog_url(url):

    def get_info(list_1):
        str_1=''
        for html_1 in list_1:
            str_1+=html_1.get_text()+','
        return str_1

    # url='http://book.zongheng.com/book/591854.html'
    html_1=requests.get(url=url)
    info_1=html_1.text
    soup_1=BeautifulSoup(info_1,'lxml')
    info_book=soup_1.select('div.book-info')
    book_label_1=get_info(info_book[0].select('div.book-label>a'))
    book_label_2=get_info(info_book[0].select('div.book-label>span>a'))
    book_label=book_label_1+book_label_2
    jian_jie=(info_book[0].select('div.book-dec.Jbook-dec.hide>p'))[0].get_text()   #小说的简介
    book_mu_url=info_book[0].select('div.btn-group>div.fr.link-group>a.all-catalog')[0]['href']   # 小说目录的网址
    print('---->{}'.format(book_label))
    print('---->{}'.format(jian_jie))

    return book_mu_url


def get_catalog(url):
    # url='http://book.zongheng.com/showchapter/591854.html'
    headers_1={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    html_2=requests.get(url=url,headers=headers_1)
    soup_2=BeautifulSoup(html_2.text,'lxml')
    list_3=soup_2.select('div.volume-list>div')
    title_list=[]
    ti_url_list=[]

    for soup_3 in list_3:
        info_text=soup_3.select('div.volume ')[0].get_text().strip('\n')  #去掉左右换行
        title_list.append(info_text)
        list_text=soup_3.select('ul.chapter-list.clearfix>li>a')
        for i in range(len(list_text)):
            list_text[i]=[list_text[i].get_text(),list_text[i]['href']]
        ti_url_list.append(list_text)

    for i in range(len(title_list)):
        print(title_list[i])
        for j in range(len(ti_url_list[i])):
            print(ti_url_list[i][j][0])

    return ti_url_list


def Write_To_Wps(ti_url_list,book_name):
    def Thread_write(ti_url_list:list,book_name:str):
        while True:
            if len(ti_url_list)==0:
                break
            list_2=ti_url_list.pop()
            while True:
                if len(list_2)==0:
                    break
                url_text=list_2.pop()
                # url_1='http://book.zongheng.com/chapter/591854/38192586.html'
                url_1=url_text[-1]
                text_name=url_text[0]
                headers_1={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
                info_4=requests.get(url=url_1,headers=headers_1).text
                soup_4=BeautifulSoup(info_4,'lxml')
                text_info=soup_4.select('div.reader_box')
                # text_name=text_info[0].select('div.title>div.title_txtbox')[0].get_text()   #小说一章的标题
                list_1=text_info[0].select('div.content>p')    #小说一章的内容
                path_1='./{}'.format(book_name)
                try:
                    os.mkdir(path_1)
                except:
                    pass
                finally:
                    str_info=''
                    for str_1 in list_1:
                        str_info+=str_1.get_text()+'\n'
                    path_2=path_1+'/{}.doc'.format(text_name)
                    print('当前线程为{1},正在下载{0}'.format(text_name,threading.current_thread().getName()))
                    text_name=' '*30+text_name+'\n'
                    try:
                        with open(path_2,'w',encoding='utf-8') as f:
                            f.write(text_name)
                            f.write(str_info)
                    except:
                        pass

    threading_list=[]
    for i in range(10):
        threading_1=threading.Thread(target=Thread_write,args=(ti_url_list,book_name,))
        threading_1.start()
        threading_list.append(threading_1)
    for i in threading_list:
        i.join()
    print('------------下载完毕！当前线程为{}'.format(threading.current_thread().getName()))


if __name__ == '__main__':
    tuple_1=matching_book()    # 这个返回的是一个元组，第一个参数是小说的网址，第二个参数是小说的名称
    url,book_name=tuple_1[0],tuple_1[1]
    catalog_url=get_catalog_url(url)    #小说目录的url
    ti_url_list=get_catalog(catalog_url)
    Write_To_Wps(ti_url_list=ti_url_list,book_name=book_name)
