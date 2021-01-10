import urllib.request

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Referer": "http://pic.netbian.com/4kmeinv/index.html"
    }
    url = 'https://www.liaoxuefeng.com/wiki/1016959663602400/1017105451316128'
    response = requests.get(url, headers=headers)
    content = BeautifulSoup(response, 'html.parser').find_all('div', class_='page-content')
    print(response)
