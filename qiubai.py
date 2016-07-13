#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-08 16:46:11
# @Author  : gufengya (gufengya@gmail.com)
# @Link    : 学习自http://cuiqingcai.com/990.html
# 本程序参考自http://cuiqingcai.com/990.html，略做修改，适合python3.

import requests,re
from bs4 import BeautifulSoup
class QSBK(object):

    def __init__(self):
        self.page = 1
        self.enable = False
        self.stories = []

    def get_page(self):
    
        url = "http://www.qiushibaike.com/hot/page/" + str(self.page)
        response = requests.get(url)
        content = response.content.decode("utf-8")
        pattern = re.compile(r'''<h2>(.+?)</h2>.*?content">(.+?)</div>(.+?)"number">(\d+)</i>.+?"number">(\d+)</i>''', re.S)
        items = re.findall(pattern, content)
        page_stories = []
        for item in items:
            haveImg = re.search("img", item[2])
            if not haveImg:
                #item[0]:作者， item[3]：点赞数，item[1]:内容
                page_stories.append([item[0], item[1].strip().replace('<br/>', '\n'), item[3]])
        return page_stories

    def load_page(self):
        if self.enable == True:
            if len(self.stories) < 1:
                page_stories = self.get_page()
                if page_stories:
                    self.stories.append(page_stories)
                    self.page += 1

    def get_onestory(self, page_stories):
        for story in page_stories:
            inp = input()
            if inp == "q":
                self.enable = False
                return
            body = "第%d页\t发布人:%s\t赞:%s\n%s" % (self.page - 1, story[0], story[2], story[1])
            print(body, "\n=========================================================================")
            
    def start(self):
        print("正在读取，按回车键查看，按q退出")
        self.enable = True
        while self.enable:
            self.load_page()
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                del self.stories[0]
                self.get_onestory(page_stories)

qsbk = QSBK()
qsbk.start()

            



