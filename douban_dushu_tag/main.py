# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote
import urllib.error
import re

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class DOUBAN:
    ### initialization
    def __init__(self, baseurl, tag, sortOrder):
        self.baseurl = baseurl
        self.tag = tag
        self.sortOrder = sortOrder
        self.tool = Tool()
        self.file = None
        self.defaultTitle = "douban_dushu_tag"
        self.floor = 1

    ### get html content, ?start=20&amp;type=T
    def getPage(self, pageNum):
        try:
            # tag has chinese char, encode it using urllib.parse.quote
            url = self.baseurl + quote(self.tag) + '?start=' + str(pageNum*20) + '&type=' + self.sortOrder
            response = urllib.request.urlopen(url)
            return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print(e.reason)
                return None

    ### get title of the tag
    def getTitle(self, page):
        pattern = re.compile('<head>.*?<title>(.*?)</title>',re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    ### get total page num, <a href="/tag/编程?start=1720&amp;type=T" >87</a>
    def getPageNum(self, page):
        pattern = re.compile('<a href=\"/tag/.*?start=.*?>(.*?)</a>',re.S)
        ## use find all because there all duplicate
        result = re.findall(pattern, page)
        if result:
            # the last element is "next page", hence second last element is the
            # total page num
            return result[-3]
        else:
            return None

    ## get content of each book
    def getContent(self, page):
        pattern = re.compile('<li class=\"subject-item\">.*?<a href=(.*?)title=(.*?)onclick=.*?<div class=\"pub\">(.*?)</div>.*?<span class=\"rating_nums\">(.*?)</span>.*?<span.*?>(.*?)</span>.*?<p>(.*?)</p>',re.S)
        items = re.findall(pattern, page)
        lst = []
        for item in items:
            # item[0] is link to the book, item[1] is title, item[2] is
            # publisher info, item[3] is review score, item[4] is no. of people
            # who have reviewed the book, item[5] is description.
            lst.append([item[0].strip(),item[1].strip(),item[2].strip(),item[3].strip(),item[4].strip(),item[5].strip()])
        return lst

    ### set title
    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(defaultTitle + '.txt', 'w+')

    def writeData(self, contents):
        for item in contents:
            floorline = '\n' + str(self.floor) + '-----------------------------------------------------------------------------------\n'
            self.file.write(floorline)
            ## write each element in the list items
            for i in range(len(item)):
                self.file.write(item[i])
            self.floor += 1

    def start(self):
        indexpage = self.getPage(0)
        pageNum = self.getPageNum(indexpage)
        title = self.getTitle(indexpage)
        self.setFileTitle(title)
        if pageNum == None:
            print('failed, please retry')
            return
        try:
            print('there are ' + pageNum + ' pages in total')
            for i in range(0,int(pageNum)):
                print('now we are at page ' + str(i) + ', please wait')
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError as e:
            print(e.message)
        finally:
            print('it is done!')

baseurl = 'https://book.douban.com/tag/'
print('please input book tag in douban: ')
## tag = raw_input()
print('please input the way you want to sort the books, input T if you want default: ')
print('input R if you want to sort by date the books publised, input S if you want to sort by user reviews')
## sortOrder = raw_input()
tag = '编程'
sortOrder = 'T'
douban = DOUBAN(baseurl, tag, sortOrder)

douban.start()
