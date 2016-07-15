#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-15 17:51:06
# @Author  : gufengya (gufengya@gmail.com)
# @Link    : http://yours.com
# @Version : $Id$

import requests, re, json
from bs4 import BeautifulSoup
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


class BDTB:
    def __init__(self, baseurl, seelz, floortag):
        self.baseurl = baseurl
        self.seelz = '?see_lz=' + str(seelz)
        self.tool = Tool()
        self.soup = None
        self.defaultTitle = u"百度贴吧"
        self.floor = 1
        self.floortag = floortag
        self.file = None

    def getHtml(self, page):
        url = self.baseurl + self.seelz + '&pn=' + str(page)
        response = requests.get(url)
        html = response.content
        return html

    def getTitle(self, html):
        title_html = self.soup.find("h3", attrs = {"class": "core_title_txt pull-left text-overflow  "})
        title = title_html["title"]
        return title

    def getPageNum(self, html):
        pageNum_html = self.soup.find("span", attrs = {"class": "red"}).find_next("span")
        pageNum = int(pageNum_html.string)
        return pageNum
        #print("共%s页" % pageNum)


    def getContent(self, html):
        contents_html = self.soup.find_all("div", attrs = {"class":"l_post l_post_bright j_l_post clearfix  "})
        contents = []
        for items in contents_html:
            item = json.loads(items["data-field"])["content"]["content"]
            content = "\n" + self.tool.replace(item) +"\n\n"
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self, contents):
        for item in contents:
            if self.floortag == "1":
                floorline = str(self.floor) + "楼===================================\n"
                self.file.write(floorline)
            self.file.write(item)
            self.floor += 1

    def start(self):
        html = self.getHtml(1)
        self.soup = BeautifulSoup(html, "html.parser")
        title = self.getTitle(html)
        pageNum = self.getPageNum(html)
        self.setFileTitle(title)
        print("该贴子共有%d页" % pageNum)
        for i in range (1, pageNum + 1):
            print("正在写入第%d页数据" % i)
            html = self.getHtml(i)
            contents = self.getContent(html)
            self.writeData(contents)
        self.file.close()
        print("写入完毕")

baseUrl = input("请输入帖子网址：")
# 'http://tieba.baidu.com/p/3138733512'
seeLZ = input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseUrl,seeLZ,floorTag)
bdtb.start()
