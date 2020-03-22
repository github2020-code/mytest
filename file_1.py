import os

path_1=input('输入路径:')
list_1=os.listdir(path_1)
dict_1 = {
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
    '零': '0'
}
list_2=[]
for i in range(len(list_1)):
    str_1=list_1[i][list_1[i].find('第')+1:list_1[i].find('章 ')]
    for j in dict_1:
        str_1=str_1.replace(j,dict_1[j])

    if '十' in str_1:
        if len(str_1) == 1:
            str_1 = '10'
        elif str_1[-1]=='十':
            str_1=str_1.replace('十','0')
        elif str_1[0]=='十':
            str_1=str_1.replace('十','1')
        else:
            str_1=str_1.replace('十','')

    if '百' in str_1:
        if len(str_1)==2:
            str_1=str_1.replace('百','00')
        else:
            str_1=str_1.replace('百','')

    str_1=list_1[i].replace(list_1[i][list_1[i].find('第')+1:list_1[i].find('章 ')],str_1)

    list_2.append(str_1)

for i in range(len(list_1)):
    print(list_1[i],list_2[i])
    os.rename(path_1+'\\'+list_1[i],path_1+'\\'+list_2[i])

