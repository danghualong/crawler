import sys

sys.path.append(".")

from src.crawler import Crawler
import re
import time

crawler = Crawler()
urlformat = "https://db.yaozh.com/instruct?p={0}&pageSize=30"
with open("./result.txt", "a") as f:
    for i in range(3108):
        url = urlformat.format((i + 1))
        print(url, "\n")
        r = crawler.request(url, method='get')
        #<a class='cl-blue' href='http://zy.yaozh.com/instruct/sms20211020/9.pdf' target='_blank'>下载1
        items = re.findall("<a.*?href=\'(.*?)\'.*?>下载1", r)
        for item in items:
            print(item, "\n")
            f.write(item + "\n")
        time.sleep(8)
