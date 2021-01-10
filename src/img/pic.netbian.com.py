# -*- coding:UTF-8 -*-
import base64
import os
import threading
from io import BytesIO

import requests
import requests as req
from lxml import etree


class downloader(object):
    def __init__(self):
        self.server = 'http://pic.netbian.com'
        self.target = 'http://pic.netbian.com/4kmeinv/'
        self.download_dir = 'F:\\图片\\彼岸图网\\'
        self.page_urls = []  # 存放页码链接
        self.html_urls = []  # 存放html链接
        self.img_urls = []  # 存放图片链接
        self.img_names = []  # 存放章节名称
        self.nums = 0  # 章节数

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Referer": "http://pic.netbian.com/"
        }

    def main(self):
        self.get_page_urls()
        for page_url in self.page_urls:
            threading.Thread(target=self.get_html_urls, args=(page_url,)).start()

    def get_page_urls(self):
        html = self.get_html(self.target)
        text = html.xpath('//div[@class="page"]/a[last() - 1]/text()')
        total_page = int(text[0])
        self.page_urls.append(self.target)
        for i in range(2, total_page + 1):
            page_url = self.target + 'index_' + str(i) + '.html'
            self.page_urls.append(page_url)

    def get_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response

    def get_html(self, url):
        response = self.get_url(url)
        if response.status_code != 200:
            print(self.target, '页面请求失败。。。')
            return
        response.encoding = 'GBK'
        html = etree.HTML(response.text)
        return html

    def get_html_urls(self, page_url):
        print(page_url, '开始下载')
        html = self.get_html(page_url)
        hrefs = html.xpath('//ul[@class="clearfix"]/li/a/@href')
        for href in hrefs:
            html_url = self.server + href
            self.get_img_url(html_url)
        print(page_url, '下载完成')

    def get_img_url(self, html_url):
        html = self.get_html(html_url)
        src = html.xpath('//div[@class="photo-pic"]/a//@src')
        name = html.xpath('//div[@class="photo-pic"]/a//@alt')
        img_url = self.server + str(src).replace('[\'', '').replace('\']', '')
        name = str(name).replace('\'', '').replace('[\'', '').replace('\']', '')
        if name == '["韩国美女组合ladies code 5k图片"]':
            name = '韩国美女组合ladies'
        self.download_image(img_url, name)

    def download_image(self, img_url, name):
        response = req.get(img_url)
        ls_f = base64.b64encode(BytesIO(response.content).read()).decode('utf-8')
        img_data = base64.b64decode(ls_f)
        img_path = self.download_dir + name + '.jpg'
        if os.path.exists(img_path) and get_img_size(img_path) > 10:
            return

        file = open(img_path, 'wb')
        file.write(img_data)
        file.close()


def get_img_size(img_path):
    size = os.path.getsize(img_path)
    size = size / float(1024)
    result = round(size, 2)
    return result


if __name__ == "__main__":
    dl = downloader()
    dl.main()
