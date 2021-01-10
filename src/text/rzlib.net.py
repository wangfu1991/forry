# -*- coding:UTF-8 -*-
import sys
import urllib.request

from bs4 import BeautifulSoup

"""
类说明:下载《日照小说网》网小说《女人如雾》
Parameters:
    无
Returns:
    无
Modify:
    2017-09-13
"""


class downloader(object):

    def __init__(self):
        self.server = 'https://www.rzlib.net/'
        self.target = 'https://www.rzlib.net/b/40/40171/'
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数

    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2017-09-13
    """

    def get_download_url(self):
        html = urllib.request.urlopen(self.target)
        div = BeautifulSoup(html, 'html.parser').find_all('div', class_='ListChapter')
        ul = BeautifulSoup(str(div[1]), 'html.parser').find_all('ul')
        li = BeautifulSoup(str(ul[0]), 'html.parser').find_all('li')
        self.nums = len(li[:])
        for each in li:
            a = BeautifulSoup(str(each), 'html.parser').find_all('a')[0]
            self.names.append(a.string)
            self.urls.append(self.server + a.get('href'))

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2017-09-13
    """

    def get_contents(self, target):
        html = urllib.request.urlopen(target)
        content = BeautifulSoup(html, 'html.parser').find_all('div', id='chapter_content')
        texts = content[0].text.replace('\xa0' * 4, '\n\n')
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2017-09-13
    """

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《女人如雾》开始下载：')
    print(dl.names[266])
    for i in range(dl.nums):
        if i >= 0:
            dl.writer(dl.names[i], '女人如雾.txt', dl.get_contents(dl.urls[i]))
            sys.stdout.write("已下载:%.3f%%\n" % float(i / dl.nums * 100))
            sys.stdout.flush()
    print('《女人如雾》下载完成')
