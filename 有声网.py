from selenium import webdriver
from lxml import etree
import requests
import os

def getDownload_url(url:str):
    driver=webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)
    url=driver.find_element_by_xpath('.//div[@id="fonhen-player"]/audio[@id="jp_audio_0"]')

    return url,driver

def Download(url:str,path:str): # 定义一个函数，用于下载一个.mp3文件
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
    content=requests.get(url=url,headers=headers)
    with open(file=path,mode='wb') as f:
        f.write(content.content)

#### 是得到自己想听的书网址

driver=webdriver.Chrome()
driver.get(url='https://www.tingshubao.com/')
driver.implicitly_wait(30)

keyword=input('请输入想听的书的名称:')
path='./{}'.format(keyword)
# 创建文件夹
try:
    os.mkdir(path=path)
except Exception as e:
    print(e)

driver.find_elements_by_xpath('.//form[@id="formsearch"]/input')[0].send_keys(keyword)  # 输入框

driver.find_elements_by_xpath('.//form[@id="formsearch"]/input')[1].click()  # 搜索按钮

text=driver.page_source  # 搜索得到的内容

driver.close()  # 关闭浏览器

html=etree.HTML(text)

L2=html.xpath('.//ul[@class="list-works"]/li')  # 列表类型

L3=list()
for i in range(len(L2)):
    L3.append(L2[i].xpath('./dl[@class="list-works-dl"]/dt/a/@href')[0])   # 进入这本书的网址
    print('【{}】----{}'.format(i+1,L2[i].xpath('./dl[@class="list-works-dl"]/dt/a/text()')[0]))  # 标题
    print(L2[i].xpath('./dl[@class="list-works-dl"]/dd[@class="list-book-des"]/text()')[0]) # 书的简介
    text2=L2[i].xpath('./dl[@class="list-works-dl"]/dd[@class="list-book-cs"]/span/text()')  # 书的作者，完结与否 等信息，
    print('作者：{}  录制人：{} 状态：{} 出版时间：{}'.format(text2[0],text2[1],text2[2],text2[3]))
    print('*'*86)

id=int(input('请输入你想听的序号：(只能1~~{})'.format(len(L2))))

#### 爬取想听的书的的内容

url='https://www.tingshubao.com'+L3[id-1]
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'}
html2=requests.get(url=url,headers=headers)
html2=etree.HTML(html2.text)
L4=html2.xpath('.//div[@id="playlist"]/ul/li')  # 列表类型，列表的长度即为总集数

url2=L4[0].xpath('./a/@href')[0]
url3=url2[:url2.rfind('-')+1]


## 下载阶段

id=input('请输入你想下载的集数范围（如1~{}）基本格式为 1,10 表示下载1·10集 ：'.format(len(L4)))
id=id.split(',')
id1,id2=int(id[0]),int(id[1])

url5='https://www.tingshubao.com'+url3+'{}.html'.format(id1-1)
L5=getDownload_url(url=url5)
href=L5[0].get_attribute('src')
e=L5[1]
Download(url=href,path=path+'./第{}集.mp3'.format(id1))
print('---已下载第{}集'.format(id1))

for i in range(id1,id2):
    url4='https://www.tingshubao.com'+url3+'{}.html'.format(i)  # 字符串的拼接
    L5=getDownload_url(url=url4)
    e.close()
    href=L5[0].get_attribute('src')
    Download(url=href,path=path+'./第{}集.mp3'.format(i+1))
    print('---已下载第{}集'.format(i+1))
    e=L5[1]

e.close()  # 关闭最后一次打开的浏览器
print('下载完毕！')
